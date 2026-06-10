"""Database seed script for local development."""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scripts.seed")


async def main() -> None:
    """Run the database seeding process."""
    logger.info("Starting database seeding...")
    # TODO: Phase 2 — Seed roles, permissions, tenant organization, and workspace
    logger.info("Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(main())
