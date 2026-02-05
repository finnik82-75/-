"""
CLI-утилита для проверки автоматического парсинга конкурентов.

Запуск из корня проекта:
  python -m backend.run_competitors
"""

import asyncio

from backend.services.parser_service import parser_service


def _clip(value: str | None, limit: int) -> str:
    if not value:
        return ""
    value = value.strip()
    return value if len(value) <= limit else value[:limit] + "…"


async def main() -> int:
    results = await parser_service.parse_competitor_urls()

    ok = 0
    fail = 0

    for url, title, h1, first_paragraph, screenshot_bytes, error in results:
        print(f"URL: {url}")
        if error:
            fail += 1
            print(f"  status: ERROR")
            print(f"  error:  {error}")
        else:
            ok += 1
            print("  status: OK")
            print(f"  title:  {_clip(title, 120)}")
            print(f"  h1:     {_clip(h1, 120)}")
            print(f"  text:   {_clip(first_paragraph, 180)}")
            kb = (len(screenshot_bytes) / 1024) if screenshot_bytes else 0
            print(f"  shot:   {kb:.1f} KB")
        print("-" * 60)

    print(f"Done. OK={ok}, ERROR={fail}, TOTAL={len(results)}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    finally:
        # На всякий случай закрываем executor сервиса.
        try:
            asyncio.run(parser_service.close())
        except Exception:
            pass

