<?php

namespace App\Entity;

use App\Repository\CarRepository;
use DateTime;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: CarRepository::class)]
class Car
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $photopath = null;

    #[ORM\Column(length: 255)]
    private ?string $name = null;

    #[ORM\Column(length: 255)]
    private ?string $model = null;

    #[ORM\Column(length: 255)]
    private ?string $year_of_production = null;

    #[ORM\Column(nullable: false)]
    private ?int $price = null;

    #[ORM\Column(length: 255)]
    private ?string $engine = null;

    #[ORM\Column(length: 255)]
    private ?string $power = null;

    #[ORM\Column(length: 255)]
    private ?string $acceleration = null;

    #[ORM\Column(length: 255)]
    private ?string $weight = null;

    #[ORM\Column(length: 255)]
    private ?string $conditioncar = null;

    #[ORM\Column(type: Types::TEXT)]
    private ?string $description = null;

    #[ORM\Column]
    private ?int $quantity = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $status = null;

    #[ORM\Column]
    private ?DateTime $creationdate = null;

    #[ORM\ManyToOne(inversedBy: 'cars')] # , cascade: ['persist', 'remove']
    #[ORM\JoinColumn(nullable: false)]
    private ?User $owner = null;


    public function getId(): ?int
    {
        return $this->id;
    }

    public function getPhotopath(): ?string
    {
        return $this->photopath;
    }

    public function setPhotopath(string $photopath): static
    {
        $this->photopath = $photopath;

        return $this;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): static
    {
        $this->name = $name;

        return $this;
    }

    public function getModel(): ?string
    {
        return $this->model;
    }

    public function setModel(string $model): static
    {
        $this->model = $model;

        return $this;
    }

    public function getYearOfProduction(): ?string
    {
        return $this->year_of_production;
    }

    public function setYearOfProduction(string $year_of_production): static
    {
        $this->year_of_production = $year_of_production;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(string $description): static
    {
        $this->description = $description;

        return $this;
    }

    public function getEngine(): ?string
    {
        return $this->engine;
    }

    public function setEngine(string $engine): static
    {
        $this->engine = $engine;

        return $this;
    }

    public function getPower(): ?string
    {
        return $this->power;
    }

    public function setPower(string $power): static
    {
        $this->power = $power;

        return $this;
    }

    public function getAcceleration(): ?string
    {
        return $this->acceleration;
    }

    public function setAcceleration(string $acceleration): static
    {
        $this->acceleration = $acceleration;

        return $this;
    }

    public function getWeight(): ?string
    {
        return $this->weight;
    }

    public function setWeight(string $weight): static
    {
        $this->weight = $weight;

        return $this;
    }

    public function getOwner(): ?User
    {
        return $this->owner;
    }

    public function setOwner(?User $owner): static
    {
        $this->owner = $owner;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getIsCart(): ?string
    {
        return $this->isCart;
    }

    /**
     * @param string|null $isCart
     */
    public function setIsCart(?string $isCart): void
    {
        $this->isCart = $isCart;
    }

    /**
     * @return int|null
     */
    public function getPrice(): ?int
    {
        return $this->price;
    }

    /**
     * @param int|null $price
     */
    public function setPrice(?int $price): void
    {
        $this->price = $price;
    }

    /**
     * @return DateTime|null
     */
    public function getCreationDate(): ?DateTime
    {
        return $this->creationdate;
    }

    /**
     * @param DateTime|null $creation_date
     */
    public function setCreationDate(?DateTime $creation_date): void
    {
        $this->creationdate = $creation_date;
    }

    /**
     * @return int|null
     */
    public function getQuantity(): ?int
    {
        return $this->quantity;
    }

    /**
     * @param int|null $quantity
     */
    public function setQuantity(?int $quantity): void
    {
        $this->quantity = $quantity;
    }

    /**
     * @return string|null
     */
    public function getConditioncar(): ?string
    {
        return $this->conditioncar;
    }

    /**
     * @param string|null $conditioncar
     */
    public function setConditioncar(?string $conditioncar): void
    {
        $this->conditioncar = $conditioncar;
    }

    /**
     * @return string|null
     */
    public function getStatus(): ?string
    {
        return $this->status;
    }

    /**
     * @param string|null $status
     */
    public function setStatus(?string $status): void
    {
        $this->status = $status;
    }
}
