from pydantic import RootModel


class NLDBSchema(RootModel):
    root: dict[str, str]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class NLTablesSummary(RootModel):
    root: dict[str, str]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
