import re

from bs4 import BeautifulSoup

from src.property_data_pipeline.parser.pydantic_models import (
    Distances,
    MainInfo,
    Parsed,
)


def parse_html(html_content: str) -> Parsed:
    """Parse the HTML content to extract required property data."""
    soup = BeautifulSoup(html_content, 'lxml')

    price = soup.find("span", class_="price-eur").text.strip()

    # Prepare main_info
    main_info_soup = soup.find("dl", class_="obj-details")
    main_info_data = dict(
        zip(
            [dt.text.strip() for dt in main_info_soup.find_all("dt")],
            [dd.text.strip() for dd in main_info_soup.find_all("dd")],
        )
    )
    main_info_data.pop('Reklama/pasiūlymas:', None)
    main_info = MainInfo(**main_info_data)

    description = soup.find("div", attrs={'id': 'collapsedText'}).text.strip()

    # Prepare distances
    distance_elements = soup.find_all("div", class_="statistic-info-cell-main")
    distances_data = {
        distance.find("span", class_="cell-text")
        .text.strip(): distance.find("span", class_="cell-data")
        .text.replace('~', '')
        .strip()
        for distance in distance_elements
    }
    distances = Distances(**distances_data)

    images = [
        image['href']
        for image in soup.find_all("a", attrs={'data-id': re.compile(r'thumb\d+')})
    ]

    map_link = soup.find("a", class_="link-obj-thumb vector-thumb-map")['href']
    coordinates = [float(coord) for coord in re.findall(r'\d+\.\d+', map_link)]
    is_map_accurate = soup.find("span", class_="map_accurate-point") is not None

    # Create a Parsed instance with the extracted data
    parsed_data = Parsed(
        price=price,
        main_info=main_info,
        description=description,
        distances=distances,
        images=images,
        coordinates=coordinates,
        is_map_accurate=is_map_accurate,
    )

    return parsed_data
