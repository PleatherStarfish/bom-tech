from components.models import (
    Component,
    ComponentSupplier,
    ComponentSupplierItem,
    ComponentManufacturer,
    Types,
    SizeStandard,
    Category,
)
from djmoney.money import Money
import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

OHMS_UNITS_MAP = {
    "": "Ω",  # Default to Ω if no unit is specified
    "K": "kΩ",
    "M": "MΩ",
}

MOUNTING_STYLES = {
    "smt": "Surface Mount",
    "th": "Through Hole",
}  # Valid mounting styles


class Command(BaseCommand):
    help = "Update database from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the CSV file with component data"
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Look up the manufacturer "Royal Ohm"
                manufacturer_name = "Royal Ohm"
                try:
                    manufacturer = ComponentManufacturer.objects.get(
                        name=manufacturer_name
                    )
                except ComponentManufacturer.DoesNotExist:
                    raise ValueError(
                        f"Manufacturer '{manufacturer_name}' does not exist in the database. Please create it before running the script."
                    )

                for row in reader:
                    try:
                        # Extract data from CSV
                        sku = row["SKU"]
                        ohms = Decimal(row["Ohms"]) if row["Ohms"] else None
                        raw_ohms_unit = (
                            row["Ohms Unit"].upper() if row["Ohms Unit"] else ""
                        )
                        ohms_unit = OHMS_UNITS_MAP.get(raw_ohms_unit, None)
                        wattage = row["Wattage"]
                        tolerance = row["Tolerance"] if "Tolerance" in row else None
                        price = Money(row["Price"], "USD") if row["Price"] else None
                        link = row["Link"]
                        mounting_style = row["Mounting Style"].lower()
                        size_name = row["Size"]
                        category_name = row["Category"]

                        # Validate Mounting Style
                        if mounting_style not in MOUNTING_STYLES:
                            raise ValueError(
                                f"Invalid Mounting Style '{mounting_style}' for SKU {sku}"
                            )

                        # Validate Ohms Unit
                        if not ohms_unit:
                            raise ValueError(
                                f"Invalid Ohms Unit '{raw_ohms_unit}' for SKU {sku}"
                            )

                        # Fetch SizeStandard
                        try:
                            size = SizeStandard.objects.get(name=size_name)
                        except SizeStandard.DoesNotExist:
                            raise ValueError(
                                f"SizeStandard '{size_name}' does not exist."
                            )

                        # Fetch Category
                        try:
                            category = Category.objects.get(name=category_name)
                        except Category.DoesNotExist:
                            raise ValueError(
                                f"Category with name '{category_name}' does not exist."
                            )

                        # Supplier setup (e.g., Tayda Electronics)
                        supplier_name = "Tayda Electronics"
                        try:
                            supplier = ComponentSupplier.objects.get(name=supplier_name)
                        except ComponentSupplier.DoesNotExist:
                            raise ValueError(
                                f"Supplier '{supplier_name}' does not exist in the database."
                            )

                        # Component type setup (e.g., Resistors)
                        component_type_name = "Resistor"
                        component_type, _ = Types.objects.get_or_create(
                            name=component_type_name
                        )

                        # Retrieve or update the Component
                        try:
                            component = Component.objects.get(
                                supplier=supplier, supplier_item_no=sku
                            )

                            # Update fields if necessary
                            updated = False
                            if component.manufacturer != manufacturer:
                                component.manufacturer = manufacturer
                                updated = True
                            if component.ohms != ohms:
                                component.ohms = ohms
                                updated = True
                            if component.ohms_unit != ohms_unit:
                                component.ohms_unit = ohms_unit
                                updated = True
                            if component.wattage != wattage:
                                component.wattage = wattage
                                updated = True
                            if component.tolerance != tolerance:
                                component.tolerance = tolerance
                                updated = True
                            if component.mounting_style != mounting_style:
                                component.mounting_style = mounting_style
                                updated = True
                            if component.size != size:
                                component.size = size
                                updated = True
                            if component.category != category:
                                component.category = category
                                updated = True
                            if component.link != link:
                                component.link = link
                                updated = True

                            if updated:
                                component.description = ""
                                component.save()
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"Updated Component: {component.description}"
                                    )
                                )

                        except Component.DoesNotExist:
                            # Create a new Component if it doesn't exist
                            component = Component.objects.create(
                                supplier=supplier,
                                supplier_item_no=sku,
                                type=component_type,
                                manufacturer=manufacturer,
                                category=category,
                                ohms=ohms,
                                ohms_unit=ohms_unit,
                                wattage=wattage,
                                tolerance=tolerance,
                                mounting_style=mounting_style,
                                size=size,
                                link=link,
                                description="",
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created Component: {component.description}"
                                )
                            )

                        # Create or update ComponentSupplierItem
                        supplier_item, supplier_item_created = (
                            ComponentSupplierItem.objects.get_or_create(
                                component=component,
                                supplier=supplier,
                                supplier_item_no=sku,
                                defaults={"price": price, "pcs": 1, "link": link},
                            )
                        )
                        if not supplier_item_created:
                            supplier_item.price = price
                            supplier_item.link = link
                            supplier_item.save()

                            self.stdout.write(
                                self.style.NOTICE(
                                    f"Updated SupplierItem: SKU {sku}, Price {price}"
                                )
                            )

                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Error processing row {row}: {e}")
                        )

            self.stdout.write(self.style.SUCCESS("Database update completed."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading CSV file: {e}"))
