# imialive
простий бот для відслідкування наявності світла вдома. надсилає повідомлення в ваш особистий канал тоді, коли воно з'являється і оновлює повідомлення кожні пару хвилин, поки є світло. було акнуально під час постійних відключень взимку 2022-2023 із-за російсько-української війни.

для того, щоб це працювало, потрібен будь який вільний комп, в біосі якого ви зможете переназначити ввімкнення по наявності електроенергії(кнопка power on), і поставити працювати цей бот по ввімкненню пк. на лінуксі це робиться через демонів. 

також в папку з ботом слід додати файл config.py і вказати всі необхідні змінні(ну і встановити всі необхідні бібліотеки за потреби)