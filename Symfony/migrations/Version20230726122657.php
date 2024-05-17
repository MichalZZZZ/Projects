<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20230726122657 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE car (id INT AUTO_INCREMENT NOT NULL, owner_id INT NOT NULL, photopath VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, model VARCHAR(255) NOT NULL, year_of_production VARCHAR(255) NOT NULL, price INT NOT NULL, engine VARCHAR(255) NOT NULL, power VARCHAR(255) NOT NULL, acceleration VARCHAR(255) NOT NULL, weight VARCHAR(255) NOT NULL, conditioncar VARCHAR(255) NOT NULL, description LONGTEXT NOT NULL, quantity INT NOT NULL, status VARCHAR(255) DEFAULT NULL, creationdate DATETIME NOT NULL, INDEX IDX_773DE69D7E3C61F9 (owner_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE opinion_seller (id INT AUTO_INCREMENT NOT NULL, user_id INT DEFAULT NULL, scale INT NOT NULL, description LONGTEXT DEFAULT NULL, loginadduser LONGTEXT NOT NULL, loginuser LONGTEXT NOT NULL, creationdate DATETIME NOT NULL, INDEX IDX_F253ED7CA76ED395 (user_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE photo (id INT AUTO_INCREMENT NOT NULL, owner_id INT DEFAULT NULL, filename VARCHAR(255) DEFAULT NULL, UNIQUE INDEX UNIQ_14B784187E3C61F9 (owner_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE special_offert (id INT AUTO_INCREMENT NOT NULL, code VARCHAR(255) NOT NULL, value DOUBLE PRECISION NOT NULL, PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE transaction (id INT AUTO_INCREMENT NOT NULL, user_id INT DEFAULT NULL, product VARCHAR(255) NOT NULL, quantity INT NOT NULL, price DOUBLE PRECISION NOT NULL, photopath VARCHAR(255) NOT NULL, creationdate DATETIME NOT NULL, userlogin VARCHAR(255) NOT NULL, useremail VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, userlastname VARCHAR(255) NOT NULL, user_phone INT NOT NULL, sellerlogin VARCHAR(255) NOT NULL, selleremail VARCHAR(255) NOT NULL, sellername VARCHAR(255) NOT NULL, sellerlastname VARCHAR(255) NOT NULL, seller_phone INT NOT NULL, seller_id INT NOT NULL, INDEX IDX_723705D1A76ED395 (user_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE `user` (id INT AUTO_INCREMENT NOT NULL, username VARCHAR(180) NOT NULL, roles JSON NOT NULL, password VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, name VARCHAR(180) NOT NULL, lastname VARCHAR(180) NOT NULL, phone VARCHAR(255) NOT NULL, creationdate DATETIME NOT NULL, UNIQUE INDEX UNIQ_8D93D649F85E0677 (username), UNIQUE INDEX UNIQ_8D93D649E7927C74 (email), UNIQUE INDEX UNIQ_8D93D649444F97DD (phone), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE messenger_messages (id BIGINT AUTO_INCREMENT NOT NULL, body LONGTEXT NOT NULL, headers LONGTEXT NOT NULL, queue_name VARCHAR(190) NOT NULL, created_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', available_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', delivered_at DATETIME DEFAULT NULL COMMENT \'(DC2Type:datetime_immutable)\', INDEX IDX_75EA56E0FB7336F0 (queue_name), INDEX IDX_75EA56E0E3BD61CE (available_at), INDEX IDX_75EA56E016BA31DB (delivered_at), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('ALTER TABLE car ADD CONSTRAINT FK_773DE69D7E3C61F9 FOREIGN KEY (owner_id) REFERENCES `user` (id)');
        $this->addSql('ALTER TABLE opinion_seller ADD CONSTRAINT FK_F253ED7CA76ED395 FOREIGN KEY (user_id) REFERENCES `user` (id)');
        $this->addSql('ALTER TABLE photo ADD CONSTRAINT FK_14B784187E3C61F9 FOREIGN KEY (owner_id) REFERENCES `user` (id)');
        $this->addSql('ALTER TABLE transaction ADD CONSTRAINT FK_723705D1A76ED395 FOREIGN KEY (user_id) REFERENCES `user` (id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE car DROP FOREIGN KEY FK_773DE69D7E3C61F9');
        $this->addSql('ALTER TABLE opinion_seller DROP FOREIGN KEY FK_F253ED7CA76ED395');
        $this->addSql('ALTER TABLE photo DROP FOREIGN KEY FK_14B784187E3C61F9');
        $this->addSql('ALTER TABLE transaction DROP FOREIGN KEY FK_723705D1A76ED395');
        $this->addSql('DROP TABLE car');
        $this->addSql('DROP TABLE opinion_seller');
        $this->addSql('DROP TABLE photo');
        $this->addSql('DROP TABLE special_offert');
        $this->addSql('DROP TABLE transaction');
        $this->addSql('DROP TABLE `user`');
        $this->addSql('DROP TABLE messenger_messages');
    }
}
