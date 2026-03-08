# 📤 Инструкция по публикации на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните форму:
   - **Repository name**: `pem08-master` (или другое имя)
   - **Description**: `Мониторинг конкурентов - AI Ассистент для анализа региональных новостных порталов`
   - **Visibility**: Выберите **Public** (публичный)
   - **НЕ** добавляйте README, .gitignore или лицензию (они уже есть)
3. Нажмите **Create repository**

## Шаг 2: Подключите локальный репозиторий к GitHub

Выполните команды (замените `YOUR_USERNAME` на ваш GitHub username):

```bash
cd C:\Users\IntelFinPro\.cursor\projects\pem08-master

# Подключите remote репозиторий
git remote add origin https://github.com/YOUR_USERNAME/pem08-master.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Отправьте код на GitHub
git push -u origin main
```

## Шаг 3: Проверьте публикацию

1. Откройте ваш репозиторий: `https://github.com/YOUR_USERNAME/pem08-master`
2. Убедитесь, что все файлы загружены
3. Проверьте, что README.md отображается корректно

## Шаг 4: Сделайте репозиторий публичным (если еще не сделали)

1. Перейдите в **Settings** репозитория
2. Прокрутите вниз до секции **Danger Zone**
3. Нажмите **Change repository visibility**
4. Выберите **Make public**
5. Подтвердите действие

## ✅ Готово!

Ваш проект теперь публично доступен на GitHub!

### Полезные ссылки после публикации:

- **Репозиторий**: `https://github.com/YOUR_USERNAME/pem08-master`
- **Issues**: `https://github.com/YOUR_USERNAME/pem08-master/issues`
- **Releases**: `https://github.com/YOUR_USERNAME/pem08-master/releases` (для публикации .exe файла)

### Дополнительно: Создайте Release с .exe файлом

1. Перейдите в **Releases** → **Create a new release**
2. Заполните:
   - **Tag**: `v1.0.0`
   - **Title**: `v1.0.0 - Initial Release`
   - **Description**: Описание версии
3. Загрузите `desktop/dist/CompetitorMonitor.exe` как asset
4. Нажмите **Publish release**
