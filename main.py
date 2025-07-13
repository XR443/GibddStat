from datetime import datetime

from GibddStatParser import load_from_gibdd
from transform.sql_transform import SqlTransformer, load_data


def main():
    current_year = datetime.now().year
    for year in range(current_year - 3, current_year + 1):
        load_from_gibdd(year=year)
    transformer = SqlTransformer(":memory:")
    load_data(transformer)
    transformer.close()


if __name__ == '__main__':
    main()
