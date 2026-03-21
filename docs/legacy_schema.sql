-- =============================================================
-- Legacy Database Schema (MySQL/MariaDB)
-- Database: asdmanagement
-- =============================================================
-- This file preserves the original SQL schema from the legacy
-- application. It is kept as reference for data migration
-- and is NOT used by the Django project.
-- =============================================================

-- acquisti (purchases by users of ASD services)
CREATE TABLE `acquisti` (
  `id_acquisto` int(11) NOT NULL AUTO_INCREMENT,
  `data_acquisto` date NOT NULL,
  `importo_acquisto` decimal(10,2) NOT NULL,
  `id_servizio` int(11) NOT NULL,
  `id_utente` int(11) NOT NULL,
  `id_movimento` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_acquisto`),
  KEY `acquisti_fk1` (`id_servizio`),
  KEY `acquisti_fk2` (`id_utente`),
  KEY `acquisti_fk3` (`id_movimento`),
  CONSTRAINT `acquisti_fk1` FOREIGN KEY (`id_servizio`) REFERENCES `servizi` (`id_servizio`),
  CONSTRAINT `acquisti_fk2` FOREIGN KEY (`id_utente`) REFERENCES `utenti` (`id_utente`),
  CONSTRAINT `acquisti_fk3` FOREIGN KEY (`id_movimento`) REFERENCES `movimenti` (`id_movimento`)
);

-- amministratori (system admins)
CREATE TABLE `amministratori` (
  `id_admin` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_admin` varchar(50) NOT NULL,
  `nome_admin` varchar(50) NOT NULL,
  `user_admin` varchar(50) NOT NULL,
  `pwd_admin` varchar(100) NOT NULL,
  PRIMARY KEY (`id_admin`)
);

-- atleti (athletes, linked to a user/guardian)
CREATE TABLE `atleti` (
  `id_atleta` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_atl` varchar(50) NOT NULL,
  `nome_atl` varchar(50) NOT NULL,
  `data_nascita` date NOT NULL,
  `stato_attivo` tinyint(1) NOT NULL,
  `id_nazione` int(11) NOT NULL,
  `id_utente` int(11) NOT NULL,
  PRIMARY KEY (`id_atleta`),
  KEY `atleti_fk1` (`id_utente`),
  KEY `atleti_fk2` (`id_nazione`),
  CONSTRAINT `atleti_fk1` FOREIGN KEY (`id_utente`) REFERENCES `utenti` (`id_utente`),
  CONSTRAINT `atleti_fk2` FOREIGN KEY (`id_nazione`) REFERENCES `nazioni` (`id_nazione`)
);

-- certificazioni (medical sport certificates)
CREATE TABLE `certificazioni` (
  `id_certificazione` int(11) NOT NULL AUTO_INCREMENT,
  `data_emissione` date NOT NULL,
  `data_scadenza` date NOT NULL,
  `cert_associata` tinyint(1) NOT NULL DEFAULT '0',
  `id_medico` int(11) NOT NULL,
  `id_atleta` int(11) NOT NULL,
  PRIMARY KEY (`id_certificazione`),
  KEY `certificazioni_fk1` (`id_atleta`),
  KEY `certificazioni_fk2` (`id_medico`),
  CONSTRAINT `certificazioni_fk1` FOREIGN KEY (`id_atleta`) REFERENCES `atleti` (`id_atleta`),
  CONSTRAINT `certificazioni_fk2` FOREIGN KEY (`id_medico`) REFERENCES `medici` (`id_medico`)
);

-- collaboratori (collaborators/staff)
CREATE TABLE `collaboratori` (
  `id_collaboratore` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_collab` varchar(50) NOT NULL,
  `nome_collab` varchar(50) NOT NULL,
  `codfiscale_collab` varchar(16) NOT NULL,
  `data_insert` date NOT NULL,
  `id_operatore` int(11) NOT NULL,
  PRIMARY KEY (`id_collaboratore`),
  KEY `collaboratori_fk1` (`id_operatore`),
  CONSTRAINT `collaboratori_fk1` FOREIGN KEY (`id_operatore`) REFERENCES `operatori` (`id_operatore`)
);

-- compensi (compensations for collaborators)
CREATE TABLE `compensi` (
  `id_compenso` int(11) NOT NULL AUTO_INCREMENT,
  `data_erogazione` date NOT NULL,
  `importo_compenso` decimal(10,2) NOT NULL,
  `id_collaboratore` int(11) NOT NULL,
  `id_movimento` int(11) NOT NULL,
  PRIMARY KEY (`id_compenso`),
  KEY `compensi_fk1` (`id_collaboratore`),
  KEY `compensi_fk2` (`id_movimento`),
  CONSTRAINT `compensi_fk1` FOREIGN KEY (`id_collaboratore`) REFERENCES `collaboratori` (`id_collaboratore`),
  CONSTRAINT `compensi_fk2` FOREIGN KEY (`id_movimento`) REFERENCES `movimenti` (`id_movimento`)
);

-- comuni (municipalities)
CREATE TABLE `comuni` (
  `id_comune` int(11) NOT NULL AUTO_INCREMENT,
  `denom_comune` varchar(150) NOT NULL,
  `id_provincia` int(11) NOT NULL,
  PRIMARY KEY (`id_comune`),
  KEY `comuni_fk1` (`id_provincia`),
  CONSTRAINT `comuni_fk1` FOREIGN KEY (`id_provincia`) REFERENCES `province` (`id_provincia`)
);

-- fatture (invoices)
CREATE TABLE `fatture` (
  `id_fattura` int(11) NOT NULL AUTO_INCREMENT,
  `descr_fattura` varchar(150) NOT NULL,
  `data_fattura` date NOT NULL,
  `num_fattura` varchar(25) NOT NULL,
  `importo_fattura` decimal(10,2) NOT NULL,
  `acquisto_vendita` tinyint(1) NOT NULL,
  `id_societa` int(11) NOT NULL,
  `id_movimento` int(11) NOT NULL,
  PRIMARY KEY (`id_fattura`),
  KEY `fatture_fk1` (`id_societa`),
  KEY `fatture_fk2` (`id_movimento`),
  CONSTRAINT `fatture_fk1` FOREIGN KEY (`id_societa`) REFERENCES `societa` (`id_societa`),
  CONSTRAINT `fatture_fk2` FOREIGN KEY (`id_movimento`) REFERENCES `movimenti` (`id_movimento`)
);

-- iscrizioni (enrollments)
CREATE TABLE `iscrizioni` (
  `id_iscrizione` int(11) NOT NULL AUTO_INCREMENT,
  `data_iscrizione` date NOT NULL,
  `iscr_associata` tinyint(1) NOT NULL DEFAULT '0',
  `id_atleta` int(11) NOT NULL,
  PRIMARY KEY (`id_iscrizione`),
  KEY `iscrizioni_fk1` (`id_atleta`),
  CONSTRAINT `iscrizioni_fk1` FOREIGN KEY (`id_atleta`) REFERENCES `atleti` (`id_atleta`)
);

-- medici (sport doctors)
CREATE TABLE `medici` (
  `id_medico` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_medico` varchar(50) NOT NULL,
  `nome_medico` varchar(50) NOT NULL,
  PRIMARY KEY (`id_medico`)
);

-- movimenti (financial movements)
CREATE TABLE `movimenti` (
  `id_movimento` int(11) NOT NULL AUTO_INCREMENT,
  `data_movimento` date NOT NULL,
  `descr_movimento` varchar(150) NOT NULL,
  `importo_movimento` decimal(10,2) NOT NULL,
  `mov_associato` tinyint(1) NOT NULL DEFAULT '0',
  `entrata_uscita` tinyint(1) NOT NULL,
  `id_tipologia` int(11) NOT NULL,
  PRIMARY KEY (`id_movimento`),
  KEY `movimenti_fk1` (`id_tipologia`),
  CONSTRAINT `movimenti_fk1` FOREIGN KEY (`id_tipologia`) REFERENCES `tipologie` (`id_tipologia`)
);

-- nazioni (countries)
CREATE TABLE `nazioni` (
  `id_nazione` int(11) NOT NULL AUTO_INCREMENT,
  `denom_nazione` varchar(75) NOT NULL,
  PRIMARY KEY (`id_nazione`)
);

-- operatori (ASD operators)
CREATE TABLE `operatori` (
  `id_operatore` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_op` varchar(50) NOT NULL,
  `nome_op` varchar(50) NOT NULL,
  `user_op` varchar(50) NOT NULL,
  `pwd_op` varchar(100) NOT NULL,
  `autorizz_op` tinyint(1) NOT NULL,
  `data_reg` date NOT NULL,
  `id_admin` int(11) NOT NULL,
  PRIMARY KEY (`id_operatore`),
  KEY `operatori` (`id_admin`),
  CONSTRAINT `operatori` FOREIGN KEY (`id_admin`) REFERENCES `amministratori` (`id_admin`)
);

-- province (provinces)
CREATE TABLE `province` (
  `id_provincia` int(11) NOT NULL AUTO_INCREMENT,
  `denom_provincia` varchar(100) NOT NULL,
  `sigla_provincia` varchar(2) NOT NULL,
  PRIMARY KEY (`id_provincia`)
);

-- servizi (services offered by the ASD)
CREATE TABLE `servizi` (
  `id_servizio` int(11) NOT NULL AUTO_INCREMENT,
  `descr_servizio` varchar(150) NOT NULL,
  `importo_servizio` decimal(10,2) NOT NULL,
  `erogazione` tinyint(1) NOT NULL DEFAULT '1',
  `id_operatore` int(11) NOT NULL,
  PRIMARY KEY (`id_servizio`),
  KEY `servizi_fk1` (`id_operatore`),
  CONSTRAINT `servizi_fk1` FOREIGN KEY (`id_operatore`) REFERENCES `operatori` (`id_operatore`)
);

-- societa (external companies for invoices)
CREATE TABLE `societa` (
  `id_societa` int(11) NOT NULL AUTO_INCREMENT,
  `rag_sociale` varchar(100) NOT NULL,
  PRIMARY KEY (`id_societa`)
);

-- tipologie (movement types)
CREATE TABLE `tipologie` (
  `id_tipologia` int(11) NOT NULL AUTO_INCREMENT,
  `descr_tipologia` varchar(50) NOT NULL,
  PRIMARY KEY (`id_tipologia`)
);

-- utenti (users/guardians who manage athletes)
CREATE TABLE `utenti` (
  `id_utente` int(11) NOT NULL AUTO_INCREMENT,
  `cognome_ut` varchar(50) NOT NULL,
  `nome_ut` varchar(50) NOT NULL,
  `nome_via` varchar(100) NOT NULL,
  `num_civico` varchar(10) NOT NULL,
  `cap` varchar(5) NOT NULL,
  `codfiscale_ut` varchar(16) NOT NULL,
  `telefono_ut` varchar(20) NOT NULL,
  `email_ut` varchar(100) NOT NULL,
  `user_ut` varchar(50) NOT NULL,
  `pwd_ut` varchar(100) NOT NULL,
  `autorizz_ut` tinyint(1) NOT NULL,
  `id_comune` int(11) NOT NULL,
  PRIMARY KEY (`id_utente`),
  KEY `utenti_fk1` (`id_comune`),
  CONSTRAINT `utenti_fk1` FOREIGN KEY (`id_comune`) REFERENCES `comuni` (`id_comune`)
);
