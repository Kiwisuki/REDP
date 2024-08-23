from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.property_data_pipeline.database.schemas import ParsedFlat
from src.property_data_pipeline.parser.parse_html import parse_html
from src.property_data_pipeline.parser.pydantic_models import Parsed


def pyd_to_orm(parsed_data: Parsed, html_id: UUID) -> ParsedFlat:
    """Insert parsed data into the database."""
    return ParsedFlat(
        price=parsed_data.price,
        house_number=parsed_data.main_info.house_number,
        apartment_number=parsed_data.main_info.apartment_number,
        area=parsed_data.main_info.area,
        room_count=parsed_data.main_info.room_count,
        floor=parsed_data.main_info.floor,
        total_floors=parsed_data.main_info.total_floors,
        year=parsed_data.main_info.year,
        building_type=parsed_data.main_info.building_type,
        heating=parsed_data.main_info.heating,
        condition=parsed_data.main_info.condition,
        energy_class=parsed_data.main_info.energy_class,
        features=parsed_data.main_info.features,
        additional_rooms=parsed_data.main_info.additional_rooms,
        additional_equipment=parsed_data.main_info.additional_equipment,
        security=parsed_data.main_info.security,
        description=parsed_data.description,
        nearest_kindergarten=parsed_data.distances.nearest_kindergarten,
        nearest_school=parsed_data.distances.nearest_school,
        nearest_store=parsed_data.distances.nearest_store,
        images=parsed_data.images,
        coordinates=parsed_data.coordinates,
        is_map_accurate=parsed_data.is_map_accurate,
        scraped_html_id=html_id,
    )


def parse_and_store_flat(html_content: str, html_id: UUID, db_session: Session):
    """Parse and store the HTML content."""
    parsed_data = parse_html(html_content)
    parsed_flat = pyd_to_orm(parsed_data, html_id)
    db_session.add(parsed_flat)
    db_session.commit()
    return parsed_flat
