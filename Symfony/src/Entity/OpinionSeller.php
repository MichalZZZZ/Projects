<?php

namespace App\Entity;

use App\Repository\OpinionSellerRepository;
use DateTime;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: OpinionSellerRepository::class)]
class OpinionSeller
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column]
    private ?int $scale = null;

    #[ORM\Column(type: Types::TEXT, nullable: true)]
    private ?string $description = null;

    #[ORM\Column(type: Types::TEXT, nullable: false)]
    private ?string $loginadduser = null;

    #[ORM\Column(type: Types::TEXT, nullable: false)]
    private ?string $loginuser = null;

    #[ORM\Column]
    private ?DateTime $creationdate = null;

    #[ORM\ManyToOne(inversedBy: 'opinionSellers')]
    private ?User $user = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getScale(): ?int
    {
        return $this->scale;
    }

    public function setScale(int $scale): static
    {
        $this->scale = $scale;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): static
    {
        $this->description = $description;

        return $this;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): static
    {
        $this->user = $user;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getLoginadduser(): ?string
    {
        return $this->loginadduser;
    }

    /**
     * @param string|null $loginadduser
     */
    public function setLoginadduser(?string $loginadduser): void
    {
        $this->loginadduser = $loginadduser;
    }

    /**
     * @return string|null
     */
    public function getLoginuser(): ?string
    {
        return $this->loginuser;
    }

    /**
     * @param string|null $loginuser
     */
    public function setLoginuser(?string $loginuser): void
    {
        $this->loginuser = $loginuser;
    }

    /**
     * @return DateTime|null
     */
    public function getCreationdate(): ?DateTime
    {
        return $this->creationdate;
    }

    /**
     * @param DateTime|null $creationdate
     */
    public function setCreationdate(?DateTime $creationdate): void
    {
        $this->creationdate = $creationdate;
    }
}
