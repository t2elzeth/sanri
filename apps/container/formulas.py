def calculate_total(
    commission,
    container_transportation,
    packaging_materials,
    wheel_recycling,
    wheel_sales,
):
    return (
        commission
        + container_transportation
        + packaging_materials
        + wheel_recycling
        - wheel_sales
    )
