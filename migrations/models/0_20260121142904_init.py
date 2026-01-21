from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "program_is_active" BOOL NOT NULL DEFAULT False,
    "last_smoked" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "modeusage" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mode_id" INT NOT NULL,
    "date_start" TIMESTAMPTZ NOT NULL,
    "date_end" TIMESTAMPTZ NOT NULL,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1v2jAQgP8K4lMndRUNUNi+BUpX1gJTC9vUqopMYoJFYlPbKUUV/322k5BXMpDYCl"
    "I/Affi3D227y68lV1iQYed6ZAic1r+WnorY+BC8SWlOS2VwXweyaWAg7GjTEFkM2acApML"
    "6QQ4DAqRBZlJ0ZwjgoUUe44jhcQUhgjbkcjD6NmDBic25FNIheLxSYgRtuArZOHP+cyYIO"
    "hYiVCRJZ+t5AZfzpWsi/mVMpRPGxsmcTwXR8bzJZ8SvLZGmEupDTGkgEO5PKeeDF9GF+QZ"
    "ZuRHGpn4IcZ8LDgBnsNj6W7JwCRY8hPRMJWgLZ/yWTuvNWrN6kWtKUxUJGtJY+WnF+XuOy"
    "oC/WF5pfSAA99CYYy4vUDKZEgZeO0poPn0Yi4phCLwNMIQWBHDUBBBjA7Onii64NVwILa5"
    "POBavV7A7Kd+177W706E1SeZDRGH2T/j/UCl+ToJNgIpr8YOEAPz4wR4XqlsAVBYbQSodE"
    "mA4okc+ncwCfH7/aCfDzHmkgI5wiLBRwuZ/LTkIMafDhNrAUWZtQzaZezZicM76em/01zb"
    "t4OWokAYt6laRS3QEoxlyZzMYpdfCsbAnC0AtYyMhmhkk21W5WpuWgIwsBUrmbHML2giPf"
    "ExYkCVs0yHiZSFTUaKvLXZR585oj4jt87YCV7M4+8ED+M67wdiBE3QhAbjgOZUxUuh48iF"
    "+fCSnil+VuB6Fn45TJoFqIbdXud+qPd+JCrkpT7sSI2mpMuU9OQiVTXXi5R+dYfXJfmz9D"
    "Dod9KFdG03fCjLmIDHiYHJwgBWPO1QHIqyOwlxzvnfYh8Dv49dfO9d9BikuUWsheyNdSzm"
    "dGR17IumVasNrVK9aNZrjUa9WVkXtKyqqLK1ut9kcUvsm1/tMsNJEnaW9BWhENn4Bi4V7a"
    "6IG2AT5tANRotRsMzhUV6FJyWURl2dgsV69ogfIJGeSApy/+VCv2/rl53y6n0GOgU2Z5YL"
    "gW8e48KdPZwJruj+Ht8Q9x/ubdGoN6fEpsA1EDPE5qIXmMObEAcCnA881z/FfywW+Fe3et"
    "ezuH3Daw0Gt4le1+qm6PZHvVZHvDqrJieMEE9AjyA7gHGDuWQGd54pUq57GCuCY/wxVWw9"
    "VezwUp56h1LvvyznSgXOVzd30AE8/w+6vNft42mMq/23s9UfNDRXVA=="
)
