from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "modeusage" ALTER COLUMN "date_end" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "modeusage" ALTER COLUMN "date_end" SET NOT NULL;"""


MODELS_STATE = (
    "eJztmFtv2jAUgP8K4qmTuooGKGxvgdKVtUDVwja1qiKTmGCR2NR22qKK/z7bSciVDCa2gt"
    "QnknNxzvlsHx/zVnaJBR12okOKzGn5a+mtjIELxUNKc1wqg/k8kksBB2NHmYLIZsw4BSYX"
    "0glwGBQiCzKTojlHBAsp9hxHCokpDBG2I5GH0ZMHDU5syKeQCsXDoxAjbMFXyMLX+cyYIO"
    "hYiVCRJb+t5AZfzJWsi/mFMpRfGxsmcTwXR8bzBZ8SvLJGmEupDTGkgEM5PKeeDF9GF+QZ"
    "ZuRHGpn4IcZ8LDgBnsNj6W7IwCRY8hPRMJWgLb/yWTutNWrN6lmtKUxUJCtJY+mnF+XuOy"
    "oC/WF5qfSAA99CYYy4PUPKZEgZeO0poPn0Yi4phCLwNMIQWBHDUBBBjBbOjii64NVwILa5"
    "XOBavV7A7Id+277Ub4+E1SeZDRGL2V/j/UCl+ToJNgIpt8YWEAPzwwR4WqlsAFBYrQWodE"
    "mA4osc+nswCfH73aCfDzHmkgI5wiLBBwuZ/LjkIMYf9xNrAUWZtQzaZezJicM76um/0lzb"
    "14OWokAYt6kaRQ3QEoxlyZzMYptfCsbAnL0AahkZDdHIOtusytXctARgYCtWMmOZX3CI9M"
    "TPiAFVzjInTKQsPGSkyFuZfZwzB3TOyKkztoIX8/gzwf3YzruBGEETNKHBOKA5VfFc6Dhy"
    "YT68pGeKnxW4noQP+0mzANWw2+vcDfXeTaJCnuvDjtRoSrpISY/OUlVzNUjpZ3d4WZKvpf"
    "tBv5MupCu74X1ZxgQ8TgxMXgxgxdMOxaEoO5MQ56z/DeYx8NvBLAZF42MS/2oSPQZpbg1r"
    "IXttGYs5HVgZ+6Jp1WpDq1TPmvVao1FvVlb1LKsqKmyt7jdZ2xLz5he7TG+ShJ0lfUEoRD"
    "a+ggtFuyviBtiEOXSDzmIUDLN/lJfhSgml0f6k4GXVesQXkEhPJAW5f7fQ79r6eae8fJ9+"
    "ToHNaeVC4Ou7uHBm96eBK9q/h9fD/Yd9W9TpzSmxKXANxAwxuegZ5vAmxIEA5wPP9U/xH4"
    "sB/tWu3nYtbn7gtQaD68RZ1+qm6PZHvVZH3JzVISeMEE9AjyA7gHGDuWQGt24pUq4fXcU7"
    "dBVb3MlTVyh1/WU5Wypwvri6hQ7g+f/P5d22D+dgXO7+OFv+BikoVwk="
)
