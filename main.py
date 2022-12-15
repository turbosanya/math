import random
import pandas as pd
import numpy as np
from tqdm import tqdm

secure_rand_gen = random.SystemRandom()


class Maker:
    def __init__(self, e, filename):
        self.e: float = e
        self.df: pd.DataFrame = None
        self.filename: str = filename
        self.sheet_num: int = None

    @property
    def df(self):
        return self.df

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, value: float):
        self._e = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value: str):
        self._filename = value

    @property
    def sheet_num(self):
        return self._sheet_num

    @sheet_num.setter
    def sheet_num(self, value: int):
        self._sheet_num = value

    def gen_data_xlsx(self, d: float, i: int, j: int, distribution=0):
        match distribution:
            case 0:
                df = pd.DataFrame.from_records(np.random.uniform(-d, d, [i, j]))
            case _:
                df = pd.DataFrame.from_records(np.random.normal())
        self.save()

    def from_excel(self, filename: str, sheet_num: int) -> pd.DataFrame:
        xl = pd.ExcelFile(filename)
        self._df = xl.parse(xl.sheet_names[sheet_num])
        return self._df

    def from_csv(self):
        pass

    def replace_all(self, sheet_name='Replace all res.xlsx'):
        for row_index, row in tqdm(self._df.iterrows()):
            for column_index, value in row.items():
                d = value * self._e
                res = secure_rand_gen.uniform(-d, d) + value
                self._df.loc[row_index, column_index] = res
        self.save(sheet_name)


    def replace_one(self, row_index, column_index, sheet_name='Result'):
        value = self.df.loc[row_index, column_index]
        d = value * self.e
        res = secure_rand_gen.uniform(-d, d) + value
        self.df.loc[row_index, column_index] = res
        self.save(sheet_name)

    def save(self, sheet_name='default_name'):
        with pd.ExcelWriter(path=self._filename, mode='a', engine='openpyxl', if_sheet_exists="replace") as writer:
            self._df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

def main():
    m = Maker(0.05, 'input.xlsx')
    m.from_excel(filename='input.xlsx', sheet_num=1)
    # print(m._df)
    m.replace_all()


if __name__ == '__main__':
    main()
