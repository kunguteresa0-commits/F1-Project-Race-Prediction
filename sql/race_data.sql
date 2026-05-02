-- Clear old features for this specific race if they exist
DELETE FROM features WHERE race_id = 1115;

-- Insert Miami GP 2026 with CORRECT IDs found in your 'drivers' table
INSERT INTO features (driver_id, race_id, grid, driver_form, career_races, is_podium)
VALUES 
('max_verstappen', 1115, 1, 1.2, 190, FALSE),
('leclerc',        1115, 2, 2.8, 130, FALSE),
('perez',          1115, 3, 3.4, 260, FALSE),
('sainz',          1115, 4, 3.1, 190, FALSE),
('piastri',        1115, 5, 4.5, 28,  FALSE),
('norris',         1115, 6, 4.2, 110, FALSE),
('russell',        1115, 7, 5.8, 110, FALSE),
('hamilton',       1115, 8, 7.2, 340, FALSE),
('alonso',         1115, 9, 6.5, 385, FALSE),
('hulkenberg',     1115, 10, 9.1, 210, FALSE),
('albon',          1115, 11, 11.5, 88, FALSE),
('stroll',         1115, 12, 12.2, 150, FALSE),
('gasly',          1115, 13, 14.5, 135, FALSE),
('ocon',           1115, 14, 13.8, 140, FALSE),
('kevin_magnussen', 1115, 15, 15.2, 170, FALSE),
('tsunoda',        1115, 16, 12.8, 70,  FALSE),
('ricciardo',      1115, 17, 13.5, 245, FALSE),
('bottas',         1115, 18, 16.2, 230, FALSE),
('zhou',           1115, 19, 17.5, 50,  FALSE),
('sargeant',       1115, 20, 18.2, 28,  FALSE);