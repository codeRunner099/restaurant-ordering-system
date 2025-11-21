DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS customer_order;
DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE menu_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category_id INTEGER NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE customer_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    table_number TEXT,
    customer_name TEXT,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL
);

CREATE TABLE order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES customer_order(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
);

INSERT INTO category (name) VALUES
('Vorspeisen'),
('Hauptgerichte'),
('Pizza'),
('Desserts'),
('Getränke');

INSERT INTO menu_item (name, description, price, category_id) VALUES
('Bruschetta', 'Geröstetes Brot mit Tomaten, Knoblauch und Basilikum', 6.50, 1),
('Minestrone', 'Italienische Gemüsesuppe mit Kräutern', 5.90, 1),
('Rinderfilet mit Rosmarinkartoffeln', 'Gegrilltes Rinderfilet mit Rotweinsauce', 24.50, 2),
('Tagliatelle al Salmone', 'Bandnudeln mit Lachs in Sahnesauce', 17.90, 2),
('Pizza Margherita', 'Tomatensauce, Mozzarella, Basilikum', 10.50, 3),
('Pizza Salami', 'Tomatensauce, Mozzarella, Salami', 12.50, 3),
('Tiramisu', 'Klassisches italienisches Dessert mit Mascarpone und Espresso', 7.20, 4),
('Panna Cotta', 'Sahnedessert mit Beerensauce', 6.80, 4),
('Hauslimonade Zitrone', 'Frisch zubereitete Limonade mit Zitrone und Minze', 4.50, 5),
('Cola 0,33 l', 'Koffeinhaltiges Erfrischungsgetränk', 3.20, 5);