

CREATE DATABASE IF NOT EXISTS sist_cinema
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sist_cinema;

-- Gêneros (ex.: Ação, Comédia)
CREATE TABLE IF NOT EXISTS generos (
  id_genero  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome       VARCHAR(60)  NOT NULL,
  descricao  VARCHAR(255) NULL,
  PRIMARY KEY (id_genero),
  UNIQUE KEY uq_generos_nome (nome)
) ENGINE=InnoDB;

-- Filmes
CREATE TABLE IF NOT EXISTS filmes (
  id_filme         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  titulo           VARCHAR(150) NOT NULL,
  sinopse          TEXT NULL,
  duracao_min      SMALLINT UNSIGNED NOT NULL,
  classificacao    ENUM('L','10','12','14','16','18') NOT NULL DEFAULT 'L',
  data_lancamento  DATE NULL,
  PRIMARY KEY (id_filme)
) ENGINE=InnoDB;

-- Tabela associativa N:N -> um filme pode ter vários gêneros
-- e um gênero pode estar em vários filmes
CREATE TABLE IF NOT EXISTS filmes_generos (
  id_filme   INT UNSIGNED NOT NULL,
  id_genero  INT UNSIGNED NOT NULL,
  PRIMARY KEY (id_filme, id_genero),
  CONSTRAINT fk_fg_filme FOREIGN KEY (id_filme)
    REFERENCES filmes (id_filme) ON DELETE CASCADE,
  CONSTRAINT fk_fg_genero FOREIGN KEY (id_genero)
    REFERENCES generos (id_genero) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Cinemas
CREATE TABLE IF NOT EXISTS cinemas (
  id_cinema  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome       VARCHAR(100) NOT NULL,
  endereco   VARCHAR(200) NOT NULL,
  cidade     VARCHAR(80)  NOT NULL,
  estado     CHAR(2)      NOT NULL,
  telefone   VARCHAR(20)  NULL,
  PRIMARY KEY (id_cinema)
) ENGINE=InnoDB;

-- Salas (1 cinema tem várias salas)
CREATE TABLE IF NOT EXISTS salas (
  id_sala     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_cinema   INT UNSIGNED NOT NULL,
  nome        VARCHAR(50)  NOT NULL,
  capacidade  SMALLINT UNSIGNED NOT NULL,
  tipo        ENUM('Convencional','VIP','IMAX','4DX','3D') NOT NULL DEFAULT 'Convencional',
  PRIMARY KEY (id_sala),
  UNIQUE KEY uq_salas_cinema_nome (id_cinema, nome),
  CONSTRAINT fk_salas_cinema FOREIGN KEY (id_cinema)
    REFERENCES cinemas (id_cinema) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Sessões: liga um filme a uma sala em um horário
-- (também é uma tabela associativa, com dados próprios: horário, idioma, preço)
CREATE TABLE IF NOT EXISTS sessoes (
  id_sessao         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_filme          INT UNSIGNED NOT NULL,
  id_sala           INT UNSIGNED NOT NULL,
  data_hora_inicio  DATETIME NOT NULL,
  idioma            ENUM('Dublado','Legendado') NOT NULL DEFAULT 'Dublado',
  formato           ENUM('2D','3D') NOT NULL DEFAULT '2D',
  preco             DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id_sessao),
  UNIQUE KEY uq_sessoes_sala_horario (id_sala, data_hora_inicio),
  CONSTRAINT fk_sessoes_filme FOREIGN KEY (id_filme)
    REFERENCES filmes (id_filme) ON DELETE RESTRICT,
  CONSTRAINT fk_sessoes_sala FOREIGN KEY (id_sala)
    REFERENCES salas (id_sala) ON DELETE CASCADE
) ENGINE=InnoDB;