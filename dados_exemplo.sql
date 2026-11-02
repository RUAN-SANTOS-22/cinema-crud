-- Dados de exemplo para o sist_cinema (carregados pelo popular.py)

USE sist_cinema;

INSERT INTO generos (id_genero, nome, descricao) VALUES
  (1, 'Ação', 'Perseguições, lutas e muita adrenalina'),
  (2, 'Comédia', 'Filmes para rir'),
  (3, 'Drama', 'Histórias intensas e emocionantes'),
  (4, 'Ficção Científica', 'Futuro, tecnologia e universos alternativos'),
  (5, 'Animação', 'Para toda a família'),
  (6, 'Aventura', 'Jornadas e descobertas'),
  (7, 'Terror', 'Suspense e sustos'),
  (8, 'Documentário', 'Histórias reais'),
  (9, 'Romance', 'Histórias de amor');

INSERT INTO filmes (id_filme, titulo, sinopse, duracao_min, classificacao, data_lancamento) VALUES
  (1, 'A Última Floresta', 'Uma expedição tenta salvar a maior floresta do planeta.', 128, '12', '2026-09-18'),
  (2, 'Rindo à Toa', 'Três amigos tentam abrir um restaurante sem saber cozinhar.', 102, '10', '2026-10-02'),
  (3, 'Cartas ao Mar', 'Uma mulher descobre cartas antigas que mudam sua família.', 115, '14', '2026-08-21'),
  (4, 'Órbita Zero', 'Uma estação espacial perde contato com a Terra.', 139, '12', '2026-10-16'),
  (5, 'Pipa e o Dragão', 'Uma menina faz amizade com um dragão filhote.', 95, 'L', '2026-07-10'),
  (6, 'A Casa do Fim da Rua', 'Uma família se muda para uma casa cheia de segredos.', 98, '16', '2026-10-30'),
  (7, 'Rios de Memória', 'Documentário sobre as comunidades ribeirinhas da Amazônia.', 87, 'L', '2026-09-05'),
  (8, 'Missão Fim de Semana', 'Dois agentes aposentados são chamados para uma última missão.', 110, '12', '2026-10-23'),
  (9, 'O Último Verão', 'Um reencontro de amigos de infância muda o rumo de duas vidas.', 121, '14', '2026-09-25'),
  (10, 'Estrela Distante', 'Uma jovem astrônoma recebe um sinal vindo de outra galáxia.', 132, '10', '2026-10-09');

-- tabela associativa: um filme pode ter vários gêneros
INSERT INTO filmes_generos (id_filme, id_genero) VALUES
  (1, 1), (1, 6),
  (2, 2),
  (3, 3), (3, 9),
  (4, 4), (4, 1),
  (5, 5), (5, 6),
  (6, 7),
  (7, 8),
  (8, 1), (8, 2),
  (9, 3), (9, 9),
  (10, 4), (10, 6);

INSERT INTO cinemas (id_cinema, nome, endereco, cidade, estado, telefone) VALUES
  (1, 'Cine Roxo Centro', 'Av. Paulista, 1000', 'São Paulo', 'SP', '(11) 3000-1000'),
  (2, 'Cine Roxo Sul', 'Rua das Acácias, 250', 'São Paulo', 'SP', '(11) 3000-2000'),
  (3, 'Cine Amarelo Plaza', 'Rua das Palmeiras, 80', 'Campinas', 'SP', '(19) 3000-3000');

INSERT INTO salas (id_sala, id_cinema, nome, capacidade, tipo) VALUES
  (1, 1, 'Sala 1', 120, 'Convencional'),
  (2, 1, 'Sala 2 - IMAX', 200, 'IMAX'),
  (3, 1, 'Sala 3 - 3D', 150, '3D'),
  (4, 2, 'Sala 1', 90, 'Convencional'),
  (5, 2, 'Sala VIP', 40, 'VIP'),
  (6, 3, 'Sala 1', 100, 'Convencional'),
  (7, 3, 'Sala 4DX', 60, '4DX');

INSERT INTO sessoes (id_filme, id_sala, data_hora_inicio, idioma, formato, preco) VALUES
  (1, 1, '2026-11-06 14:00:00', 'Dublado', '2D', 30.00),
  (1, 1, '2026-11-06 19:00:00', 'Legendado', '2D', 34.00),
  (8, 1, '2026-11-07 16:30:00', 'Dublado', '2D', 32.00),
  (4, 2, '2026-11-06 20:00:00', 'Legendado', '3D', 52.00),
  (4, 2, '2026-11-07 15:00:00', 'Dublado', '3D', 48.00),
  (10, 3, '2026-11-07 18:00:00', 'Dublado', '3D', 42.00),
  (5, 3, '2026-11-08 13:30:00', 'Dublado', '3D', 38.00),
  (2, 4, '2026-11-06 18:30:00', 'Dublado', '2D', 28.00),
  (3, 4, '2026-11-07 20:30:00', 'Legendado', '2D', 30.00),
  (9, 4, '2026-11-08 17:00:00', 'Dublado', '2D', 30.00),
  (3, 5, '2026-11-06 21:00:00', 'Legendado', '2D', 58.00),
  (9, 5, '2026-11-07 19:00:00', 'Legendado', '2D', 58.00),
  (6, 6, '2026-11-06 22:00:00', 'Dublado', '2D', 28.00),
  (7, 6, '2026-11-07 15:30:00', 'Dublado', '2D', 22.00),
  (2, 6, '2026-11-08 19:30:00', 'Dublado', '2D', 28.00),
  (10, 7, '2026-11-07 20:00:00', 'Dublado', '2D', 56.00),
  (8, 7, '2026-11-08 21:00:00', 'Dublado', '2D', 54.00);