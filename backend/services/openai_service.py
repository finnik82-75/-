"""
Сервис для работы с ProxyAPI (OpenAI-совместимый API)
https://proxyapi.ru/docs/openai-text-generation
"""
import base64
import json
import re
import time
import logging
from typing import Optional

from openai import OpenAI

from backend.config import settings
from backend.models.schemas import CompetitorAnalysis, ImageAnalysis

# Логгер для сервиса
logger = logging.getLogger("competitor_monitor.openai")


class OpenAIService:
    """Сервис для анализа через ProxyAPI"""
    
    def __init__(self):
        logger.info("=" * 50)
        logger.info("Инициализация OpenAI сервиса")
        logger.info(f"  Base URL: {settings.proxy_api_base_url}")
        logger.info(f"  Модель текста: {settings.openai_model}")
        logger.info(f"  Модель vision: {settings.openai_vision_model}")
        logger.info(f"  API ключ: {'*' * 10}...{settings.proxy_api_key[-4:] if settings.proxy_api_key else 'НЕ ЗАДАН'}")
        
        # ProxyAPI - OpenAI-совместимый API для России
        self.client = OpenAI(
            api_key=settings.proxy_api_key,
            base_url=settings.proxy_api_base_url
        )
        self.model = settings.openai_model
        self.vision_model = settings.openai_vision_model
        
        logger.info("OpenAI сервис инициализирован успешно ✓")
        logger.info("=" * 50)
    
    def _parse_json_response(self, content: str) -> dict:
        """Извлечь JSON из ответа модели"""
        logger.debug(f"Парсинг JSON ответа, длина: {len(content)} символов")
        
        # Пробуем найти JSON в markdown блоке
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if json_match:
            content = json_match.group(1)
            logger.debug("JSON найден в markdown блоке")
        
        # Пробуем найти JSON объект
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            content = json_match.group(0)
            logger.debug("JSON объект извлечён")
        
        try:
            result = json.loads(content)
            logger.debug(f"JSON успешно распарсен, ключей: {len(result)}")
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"Ошибка парсинга JSON: {e}")
            logger.debug(f"Проблемный контент: {content[:200]}...")
            return {}
    
    async def analyze_text(self, text: str) -> CompetitorAnalysis:
        """Анализ текста конкурента"""
        logger.info("=" * 50)
        logger.info("📝 АНАЛИЗ ТЕКСТА КОНКУРЕНТА")
        logger.info(f"  Длина текста: {len(text)} символов")
        logger.info(f"  Превью: {text[:100]}...")
        logger.info(f"  Модель: {self.model}")
        
        system_prompt = """Ты — аналитик региональных СМИ.

На основе заголовка, h1, текста и визуального контента сайта:

Верни строго JSON:

{
  "strengths": ["Сильная сторона 1", "Сильная сторона 2"],
  "weaknesses": ["Слабая сторона 1", "Слабая сторона 2"],
  "unique_offers": ["Особенность портала 1"],
  "recommendations": ["Рекомендация 1", "Рекомендация 2"],
  "summary": "Общий вывод о редакционной политике и повестке"
}

Пиши на русском языке.
"""

        start_time = time.time()
        logger.info("  Отправка запроса к API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Проанализируй текст конкурента:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            logger.debug(f"  Использовано токенов: {response.usage.total_tokens if response.usage else 'N/A'}")
            
            data = self._parse_json_response(content)
            
            result = CompetitorAnalysis(
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                unique_offers=data.get("unique_offers", []),
                recommendations=data.get("recommendations", []),
                summary=data.get("summary", "")
            )
            
            logger.info(f"  Результат: {len(result.strengths)} сильных, {len(result.weaknesses)} слабых сторон")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise
    
    async def analyze_image(self, image_base64: str, mime_type: str = "image/jpeg") -> ImageAnalysis:
        """Анализ изображения (баннер, сайт, упаковка)"""
        logger.info("=" * 50)
        logger.info("🖼️ АНАЛИЗ ИЗОБРАЖЕНИЯ")
        logger.info(f"  Размер base64: {len(image_base64)} символов")
        logger.info(f"  MIME тип: {mime_type}")
        logger.info(f"  Модель: {self.vision_model}")
        
        system_prompt = """Ты — профессиональный медиа-аналитик, специализирующийся на региональных новостных СМИ.

Тебе предоставлен скриншот главной страницы новостного портала.

Проанализируй сайт и верни строго JSON:

{
  "description": "Краткое описание портала и его визуальной структуры",
  "marketing_insights": [
    "Ключевые темы повестки",
    "Редакционные акценты",
    "Эмоциональный фон"
  ],
  "visual_style_score": 1-10,
  "visual_style_analysis": "Описание визуального стиля и подачи",
  "recommendations": [
    "Рекомендация 1",
    "Рекомендация 2"
  ]
}

Пиши на русском языке.
Будь аналитичен и опирайся на визуальные и текстовые элементы.
"""


        start_time = time.time()
        logger.info("  Отправка запроса к Vision API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Проанализируй этот скриншот главной страницы регионального новостного портала:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            
            data = self._parse_json_response(content)
            
            result = ImageAnalysis(
                description=data.get("description", ""),
                marketing_insights=data.get("marketing_insights", []),
                visual_style_score=data.get("visual_style_score", 5),
                visual_style_analysis=data.get("visual_style_analysis", ""),
                recommendations=data.get("recommendations", [])
            )
            
            logger.info(f"  Результат: оценка стиля {result.visual_style_score}/10")
            logger.info(f"  Инсайтов: {len(result.marketing_insights)}, рекомендаций: {len(result.recommendations)}")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка Vision API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise
    
    async def analyze_parsed_content(
        self, 
        title: Optional[str], 
        h1: Optional[str], 
        paragraph: Optional[str]
    ) -> CompetitorAnalysis:
        """Анализ распарсенного контента сайта"""
        logger.info("📄 Анализ распарсенного контента")
        logger.info(f"  Title: {title[:50] if title else 'N/A'}...")
        logger.info(f"  H1: {h1[:50] if h1 else 'N/A'}...")
        logger.info(f"  Абзац: {paragraph[:50] if paragraph else 'N/A'}...")
        
        content_parts = []
        if title:
            content_parts.append(f"Заголовок страницы (title): {title}")
        if h1:
            content_parts.append(f"Главный заголовок (H1): {h1}")
        if paragraph:
            content_parts.append(f"Первый абзац: {paragraph}")
        
        combined_text = "\n\n".join(content_parts)
        
        if not combined_text.strip():
            logger.warning("  ⚠ Контент пустой, возвращаем пустой анализ")
            return CompetitorAnalysis(
                summary="Не удалось извлечь контент для анализа"
            )
        
        return await self.analyze_text(combined_text)
    
    async def analyze_website_screenshot(
        self,
        screenshot_base64: str,
        url: str,
        title: Optional[str] = None,
        h1: Optional[str] = None,
        first_paragraph: Optional[str] = None
    ) -> CompetitorAnalysis:
        """Комплексный анализ сайта конкурента по скриншоту"""
        logger.info("=" * 50)
        logger.info("🌐 КОМПЛЕКСНЫЙ АНАЛИЗ САЙТА")
        logger.info(f"  URL: {url}")
        logger.info(f"  Title: {title[:50] if title else 'N/A'}...")
        logger.info(f"  H1: {h1[:50] if h1 else 'N/A'}...")
        logger.info(f"  Размер скриншота: {len(screenshot_base64)} символов base64")
        logger.info(f"  Модель: {self.vision_model}")
        
        # Формируем контекст из извлечённых данных
        context_parts = [f"URL сайта: {url}"]
        if title:
            context_parts.append(f"Title страницы: {title}")
        if h1:
            context_parts.append(f"Главный заголовок (H1): {h1}")
        if first_paragraph:
            context_parts.append(f"Текст на странице: {first_paragraph[:300]}")
        
        context = "\n".join(context_parts)
        logger.debug(f"  Контекст:\n{context}")
        
        system_prompt = """Ты — аналитик региональных СМИ.

На основе заголовка, h1, текста и визуального контента сайта:

Верни строго JSON:

{
  "strengths": ["Сильная сторона портала"],
  "weaknesses": ["Слабая сторона портала"],
  "unique_offers": ["Отличительная особенность или формат подачи"],
  "recommendations": ["Рекомендация по улучшению"],
  "summary": "Общий вывод о редакционной политике и месте портала в региональной повестке"
}

Пиши на русском языке.
Будь аналитичен и опирайся на визуальный и текстовый контекст.
"""


        start_time = time.time()
        logger.info("  Отправка скриншота в Vision API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Проведи комплексный конкурентный анализ этого сайта:\n\n{context}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            
            data = self._parse_json_response(content)
            
            result = CompetitorAnalysis(
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                unique_offers=data.get("unique_offers", []),
                recommendations=data.get("recommendations", []),
                summary=data.get("summary", "")
            )
            
            logger.info(f"  Результат:")
            logger.info(f"    - Сильных сторон: {len(result.strengths)}")
            logger.info(f"    - Слабых сторон: {len(result.weaknesses)}")
            logger.info(f"    - УТП: {len(result.unique_offers)}")
            logger.info(f"    - Рекомендаций: {len(result.recommendations)}")
            logger.info(f"  Резюме: {result.summary[:100]}...")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка Vision API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise


# Глобальный экземпляр
logger.info("Создание глобального экземпляра OpenAI сервиса...")
openai_service = OpenAIService()
