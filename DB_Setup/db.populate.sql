USE Mood_Tracker;

USE Mood_Tracker;

INSERT INTO Users
(First_Name, Family_Name, User_Name, Email, Password)
VALUES
('John', 'Doe', 'JoDoe', 'johndoes@example.com', 'password123'),
('Lucy', 'Smith', 'LSmith', 'lsmith@example.com', 'hello123');


INSERT INTO Entries
(User_ID, Entry_Date, Emotion, Giph_URL, Choice_J_or_Q, Response_J_or_Q, Diary_Entry)
VALUES
(1, 20240601, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(2, 20240601, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240531, 'frustrated', 'Giph_URL', 'Test choice', 'Test response', 'Super frustrated!'),
(1, 20240530, 'sad', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel sad!'),
(1, 20240529, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240528, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240527, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240526, 'frustrated', 'Giph_URL', 'Test choice', 'Test response', 'Super frustrated!'),
(1, 20240525, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240524, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240523, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240522, 'frustrated', 'Giph_URL', 'Test choice', 'Test response', 'Super frustrated!'),
(1, 20240521, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240520, 'angry', 'Giph_URL', 'Test choice', 'Test response', 'GRRRR!'),
(1, 20240519, 'sad', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel sad!'),
(1, 20240518, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240517, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240516, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240515, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240514, 'angry', 'Giph_URL', 'Test choice', 'Test response', 'GRRRR!'),
(1, 20240513, 'angry', 'Giph_URL', 'Test choice', 'Test response', 'GRRRR!'),
(1, 20240512, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240511, 'worried', 'Giph_URL', 'Test choice', 'Test response', 'I am worried!'),
(1, 20240510, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240509, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240508, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240507, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!'),
(1, 20240506, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240505, 'calm', 'Giph_URL', 'Test choice', 'Test response', 'Zen!'),
(1, 20240504, 'sad', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel sad!'),
(1, 20240503, 'frustrated', 'Giph_URL', 'Test choice', 'Test response', 'Super frustrated!'),
(1, 20240502, 'frustrated', 'Giph_URL', 'Test choice', 'Test response', 'Super frustrated!'),
(1, 20240501, 'happy', 'Giph_URL', 'Test choice', 'Test response', 'Today I feel happy!');