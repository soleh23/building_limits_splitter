CREATE_SPLITS_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS splits(
        id SERIAL PRIMARY KEY,
        building_limits JSONB NOT NULL,
        height_plateus JSONB NOT NULL,
        split_building_limits JSONB NOT NULL
    );
    """
)

INSERT_SPLITS = (
    """
    INSERT INTO splits (building_limits, height_plateus, split_building_limits) VALUES (%s, %s, %s);
    """
)

SELECT_SPLITS = (
    """
    SELECT (split_building_limits) FROM splits WHERE building_limits = %s AND height_plateus = %s;
    """
)

COUNT_ROWS = (
    """
    SELECT count (*) FROM splits;
    """
)

DELETE_ALL = (
    """
    DELETE FROM splits;
    """
)