<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20240724110036 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE bugs (id INT AUTO_INCREMENT NOT NULL, description VARCHAR(255) NOT NULL, assignee VARCHAR(50) DEFAULT NULL, priority VARCHAR(50) DEFAULT NULL, status VARCHAR(50) DEFAULT NULL, timestamp DATETIME NOT NULL, url LONGTEXT DEFAULT NULL, selector LONGTEXT DEFAULT NULL, user_agent LONGTEXT DEFAULT NULL, platform LONGTEXT DEFAULT NULL, screen_resolution LONGTEXT DEFAULT NULL, window_size VARCHAR(50) NOT NULL, attachment LONGTEXT DEFAULT NULL, types VARCHAR(20) DEFAULT NULL, PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE messenger_messages (id BIGINT AUTO_INCREMENT NOT NULL, body LONGTEXT NOT NULL, headers LONGTEXT NOT NULL, queue_name VARCHAR(190) NOT NULL, created_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', available_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', delivered_at DATETIME DEFAULT NULL COMMENT \'(DC2Type:datetime_immutable)\', INDEX IDX_75EA56E0FB7336F0 (queue_name), INDEX IDX_75EA56E0E3BD61CE (available_at), INDEX IDX_75EA56E016BA31DB (delivered_at), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('DROP TABLE tasks');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE tasks (ID INT AUTO_INCREMENT NOT NULL, description TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, assignee VARCHAR(50) CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, priority VARCHAR(50) CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, status VARCHAR(50) CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, timestamp DATETIME NOT NULL, url TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, selector TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, userAgent TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, platform TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, screenResolution TEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, windowSize VARCHAR(50) CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, attachment LONGTEXT CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, types VARCHAR(20) CHARACTER SET utf8mb4 NOT NULL COLLATE `utf8mb4_general_ci`, PRIMARY KEY(ID)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_general_ci` ENGINE = InnoDB COMMENT = \'\' ');
        $this->addSql('DROP TABLE bugs');
        $this->addSql('DROP TABLE messenger_messages');
    }
}
