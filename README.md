# Moderation-bot-discord
Старый бот модерации публичного сервера сам не знаю от куда (привязка под правила)
База данных: MongoDB

**Накидайте звёзд на репозиторий плз)**

Установка:
- Вся настройка происходит в `client/config.py`

Пояснения:
- TOKEN - ваш токен
- GUILD_ID - ID вашего сервера
- MOD_LOGS - ID канала с логами
- SWEETNESS - самая высшая роль ID роли
- ADMINISTRATOR - администратор ID роли
- M_WARDEN - кураторы ID роли
- M_HELPER - мастера ID роли
- WARDEN - модераторы ID роли
- HELPER - контролы или ещё раз модераторы ID роли
- STAFF_ROLE - роль персонала
- MALE - мальчик
- FEMALE - девочка
- TEXT_MUTE - ID роли текстового мута
- VOICE_MUTE - ID роли мута в голосовых каналах
- BAN - ID роли бана
- Временные роли
- TEXT_WARN - ID роли предупреждения текстового мута
- VOICE_WARN - ID роль предупреждения голосового мута
- BAN_WARN - ID роль предупреждения бана
- MONGO - URI MONGO DB


# Гайд как получить MONGO_DB 
примечание, используйте впн чтобы зайти на сайт с снг
1. Зайдите на сайт [MongoDB](https://www.mongodb.com)
2. Зарегистрируйтесь или авторизируйтесь на сайте
3. Создайте новый проект ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/000eb5ba-a0ab-4c07-bc26-283cb0ab7142)
4. Придумайте ему название и нажите `Next` ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/6f444d85-c023-4cf5-b986-6c41b621bf0c)
5. Далее нажмите `Create Project` ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/82ff7686-0f68-4110-9eec-71ba6867b36b)
6. Дальше создаём кластер ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/80ab7502-ada1-480d-97fd-beae0e39e0bc)
7. Берём бесплатный кластер и даём ему название ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/7b57ba8c-4c5e-407e-b34c-a7bf06e2e44e)
8. Создаём кластер и придумываем никнейм пользователя и пароль, вводим и нажимаем `Create DataBase User` или что то подобное
9. После кликаем на `Choose a connect method` ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/45c13a16-4f4e-461c-a837-7d2082ac369b)
10. Выбираем Compass ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/7480988e-a89d-4f98-8d40-a25d075a4d14)
11. Находим строку с именем вашего аккаунта и паролем или там будет `<password>` ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/1a7027e0-bc83-437c-acec-71238e6bed7b)
12. Копируем и вставляем в проект.
13. Заходим в эту вкладку ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/3fc71bf8-4f27-4b7c-b57f-199a736d1c5e)
14. Далее добавляем `0.0.0.0/0` и удаляем свой айпи ![image](https://github.com/Fequme/Moderation-bot-discord/assets/142742415/a92650e7-bf5c-44bf-94a9-f39730036a0c)






