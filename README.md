# Avito

## Описание функциональных требований

Система предоставляет следующие возможности: 

### Управление учетной записью

•   **Регистрация пользователей:** Создание профиля с основной информацией.  
•   **Авторизация:** Безопасный вход в систему с использованием логина и пароля или других методов аутентификации.  
•   **Восстановление доступа:** Процесс восстановления забытого пароля через подтверждение личности.  
•   **Управление профилем:** Редактирование личной информации, контактных данных и настроек уведомлений.  

### Публикация и редактирование объявлений

•   **Создание объявлений о товарах:** Пользователь может размещать объявлений о товарах.  
•   **Создание объявлений об услугах:** Пользователь может размещать объявлений об услугах.  
•   **Создание объявлений о вакансиях:** Пользователь может размещать объявлений о вакансиях.  
•   **Создание объявлений о недвижимости :** Пользователь может размещать объявлений о недвижимости.    
•   **Редактирование объявлений:** Изменение опубликованных объявлений для актуализации информации и добавления новых деталей.  
•   **Удаление объявлений:** Снятие объявлений с публикации.  

### Поиск и просмотр объявлений

•   **Поиск по ключевым словам:** Поиск объявлений по названию, описанию и другим релевантным атрибутам.  
•   **Фильтрация по параметрам:** Фильтрация результатов поиска по цене, дате, местоположению, категории и другим критериям.  
•   **Сортировка результатов:** Сортировка объявлений по популярности, цене, дате и другим параметрам.  
•   **Просмотр объявлений:** Отображение подробной информации об объявлении, включая описание, фотографии, контактные данные продавца/поставщика услуг.  
•   **Карта объявлений:** Отображение объявлений на карте с указанием местоположения.  

### Взаимодействие между пользователями

•   **Обмен сообщениями:** Отправка и получение личных сообщений для обсуждения деталей объявлений.  
•   **Отзывы:** Возможность оставлять отзывы для других пользователей.  
•   **Рейтинги:** Возможность оценить продавца.  
•   **Жалобы на объявления:** Механизм для сообщения о подозрительных или нарушающих правила объявлениях.  
•   **Блокировка пользователей:** Возможность заблокировать пользователя для предотвращения дальнейшего взаимодействия.  

### Безопасность и модерация

•   **Модерация объявлений:** Проверка объявлений на соответствие правилам платформы.  
•   **Фильтрация спама:** Механизмы для автоматического и ручного(жалоба) выявления и удаления спама.  
•   **Защита от мошенничества:** Механизмы для автоматического и ручного(жалоба) выявления и удаления мошеннических объявлений.  
•   **Безопасная сделка:** Приложение предоставляет сервис безопасной сделки для защиты прав покупателей и продавцов.   

### Служба поддержки
•   **Телефонная поддержка:** Возможность обратится в центр поддержки по телефону.  
•   **Чат поддержки:** Онлайн чат со службой поддержки.  

### Уведомления
•   **Уведомления о новых сообщениях:** Уведомления о новых сообщениях от других пользователей.  
•   **Уведомления об изменениях статуса объявления:** Уведомления об изменениях статуса объявления.  
•   **Отключить уведомления:** Отключает все уведомления.  
•   **Фильтр уведомлений:** Возможность настроить приходящие уведомления.  


### Аналитика и отчетность
•   **Статистика просмотров объявлений:** Предоставление пользователям статистики просмотров их объявлений.      
•   **Анализ поведения пользователей:** Отдел аналитиков собирает информацию о поведениях пользователей на платформе для улучшения работы.  

```plantuml
' Сущности пользователей и аутентификации
entity User {
  * user_id: INT <<PK>>
  --
  * username: VARCHAR(50)
  * email: VARCHAR(100) <<UNIQUE>>
  * phone: VARCHAR(20) <<UNIQUE>>
  * password_hash: VARCHAR(255)
  * registration_date: DATETIME
  last_login: DATETIME
  is_active: BOOLEAN
  is_blocked: BOOLEAN
}

entity UserProfile {
  * profile_id: INT <<PK>>
  * user_id: INT <<FK>>
  --
  first_name: VARCHAR(50)
  last_name: VARCHAR(50)
  avatar_url: VARCHAR(255)
  about: TEXT
  rating: DECIMAL(3,2)
}

entity PasswordReset {
  * reset_id: INT <<PK>>
  * user_id: INT <<FK>>
  --
  token: VARCHAR(255)
  expiration_date: DATETIME
  is_used: BOOLEAN
}

' Сущности объявлений
entity Advertisement {
  * ad_id: INT <<PK>>
  * user_id: INT <<FK>>
  * category_id: INT <<FK>>
  * location_id: INT <<FK>>
  * status_id: INT <<FK>>
  --
  * title: VARCHAR(100)
  * description: TEXT
  * price: DECIMAL(12,2)
  * creation_date: DATETIME
  modification_date: DATETIME
  views_count: INT
}

entity AdCategory {
  * category_id: INT <<PK>>
  * parent_id: INT <<FK>>
  --
  * name: VARCHAR(50)
  description: TEXT
}

entity AdStatus {
  * status_id: INT <<PK>>
  --
  * name: VARCHAR(20)
  description: TEXT
}

entity AdType {
  * type_id: INT <<PK>>
  --
  * name: VARCHAR(20)
}

entity AdPhoto {
  * photo_id: INT <<PK>>
  * ad_id: INT <<FK>>
  --
  * photo_url: VARCHAR(255)
  is_main: BOOLEAN
  upload_date: DATETIME
}

' Специализированные типы объявлений(для type_id)
entity ProductAd {
  * ad_id: INT <<PK>> <<FK>>
  --
  brand: VARCHAR(50)
  model: VARCHAR(50)
  condition: VARCHAR(20)
  warranty: BOOLEAN
}

entity ServiceAd {
  * ad_id: INT <<PK>> <<FK>>
  --
  service_type: VARCHAR(50)
  experience: VARCHAR(50)
  availability: VARCHAR(50)
}

entity JobAd {
  * ad_id: INT <<PK>> <<FK>>
  --
  position: VARCHAR(100)
  employment_type: VARCHAR(50)
  experience_required: VARCHAR(50)
  salary_from: DECIMAL(12,2)
  salary_to: DECIMAL(12,2)
}

entity RealEstateAd {
  * ad_id: INT <<PK>> <<FK>>
  --
  property_type: VARCHAR(50)
  area: DECIMAL(10,2)
  rooms: INT
  floor: INT
  total_floors: INT
}

' Локации
entity Location {
  * location_id: INT <<PK>>
  * parent_id: INT <<FK>>
  --
  * name: VARCHAR(100)
  type: VARCHAR(20)
  coordinates: POINT
}

' Взаимодействия
entity Message {
  * message_id: INT <<PK>>
  * sender_id: INT <<FK>>
  * recipient_id: INT <<FK>>
  * conversation_id: INT <<FK>>
  --
  * content: TEXT
  * send_date: DATETIME
  is_read: BOOLEAN
}

entity Conversation {
  * conversation_id: INT <<PK>>
  * ad_id: INT <<FK>>
  --
  start_date: DATETIME
  last_message_date: DATETIME
}

entity Review {
  * review_id: INT <<PK>>
  * reviewer_id: INT <<FK>>
  * reviewed_user_id: INT <<FK>>
  * ad_id: INT <<FK>>
  --
  * rating: INT
  comment: TEXT
  creation_date: DATETIME
}

entity Complaint {
  * complaint_id: INT <<PK>>
  * reporter_id: INT <<FK>>
  * ad_id: INT <<FK>>
  * complaint_type_id: INT <<FK>>
  --
  description: TEXT
  status: VARCHAR(20)
  creation_date: DATETIME
  resolution_date: DATETIME
}

entity ComplaintType {
  * type_id: INT <<PK>>
  --
  * name: VARCHAR(50)
  description: TEXT
}

' Безопасные сделки
entity SafeDeal {
  * deal_id: INT <<PK>>
  * buyer_id: INT <<FK>>
  * seller_id: INT <<FK>>
  * ad_id: INT <<FK>>
  --
  amount: DECIMAL(12,2)
  status: VARCHAR(20)
  creation_date: DATETIME
  completion_date: DATETIME
}

' Уведомления
entity Notification {
  * notification_id: INT <<PK>>
  * user_id: INT <<FK>>
  * notification_type_id: INT <<FK>>
  --
  content: TEXT
  is_read: BOOLEAN
  creation_date: DATETIME
  related_entity_id: INT
  related_entity_type: VARCHAR(50)
}

entity NotificationType {
  * type_id: INT <<PK>>
  --
  * name: VARCHAR(50)
  template: TEXT
}

entity NotificationSettings {
  * settings_id: INT <<PK>>
  * user_id: INT <<FK>>
  --
  email_notifications: BOOLEAN
  push_notifications: BOOLEAN
  sms_notifications: BOOLEAN
}

' Поддержка
entity SupportTicket {
  * ticket_id: INT <<PK>>
  * user_id: INT <<FK>>
  * ticket_type_id: INT <<FK>>
  --
  subject: VARCHAR(100)
  description: TEXT
  status: VARCHAR(20)
  creation_date: DATETIME
  resolution_date: DATETIME
}

entity SupportTicketType {
  * type_id: INT <<PK>>
  --
  * name: VARCHAR(50)
  description: TEXT
}

' Аналитика
entity AdStatistic {
  * stat_id: INT <<PK>>
  * ad_id: INT <<FK>>
  --
  date: DATE
  views: INT
  contacts: INT
  favorites: INT
}

entity UserActivity {
  * activity_id: INT <<PK>>
  * user_id: INT <<FK>>
  --
  date: DATE
  ads_viewed: INT
  ads_created: INT
  messages_sent: INT
  searches_performed: INT
}

' Связи
User ||--o{ UserProfile
User ||--o{ PasswordReset
User ||--o{ Advertisement
User ||--o{ Message as sender
User ||--o{ Message as recipient
User ||--o{ Review as reviewer
User ||--o{ Review as reviewed_user
User ||--o{ Complaint
User ||--o{ SafeDeal as buyer
User ||--o{ SafeDeal as seller
User ||--o{ Notification
User ||--o{ NotificationSettings
User ||--o{ SupportTicket
User ||--o{ UserActivity

Advertisement }|--|| AdCategory
Advertisement }|--|| AdStatus
Advertisement }|--|| Location
Advertisement }|--|| AdType
Advertisement ||--o{ AdPhoto
Advertisement ||--o| ProductAd
Advertisement ||--o| ServiceAd
Advertisement ||--o| JobAd
Advertisement ||--o| RealEstateAd
Advertisement ||--o{ Message
Advertisement ||--o{ Review
Advertisement ||--o{ Complaint
Advertisement ||--o{ SafeDeal
Advertisement ||--o{ AdStatistic

AdCategory }|--o{ AdCategory

Location }|--o{ Location

Conversation ||--o{ Message

Complaint }|--|| ComplaintType

Notification }|--|| NotificationType

SupportTicket }|--|| SupportTicketType
```