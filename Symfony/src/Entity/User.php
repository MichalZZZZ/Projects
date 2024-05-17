<?php

namespace App\Entity;

use App\Repository\UserRepository;
use DateTime;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\Constraints\Length;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: '`user`')]
#[UniqueEntity(fields: ['username'], message: 'Ten login jest już zajęty')]
#[UniqueEntity(fields: ['email'], message: 'Ten adres email jest już zajęty')]
#[UniqueEntity(fields: ['phone'], message: 'Ten numer telefonu jest już w użyciu')]


class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 180, unique: true)]
    private ?string $username = null;

    #[ORM\Column]
    private array $roles = [];

    /**
     * @var string The hashed password
     */
    #[ORM\Column]
    private ?string $password = null;

    #[ORM\Column(unique: true)]
    private ?string $email = null;

    #[ORM\Column(length: 180)]
    private ?string $name = null;

    #[ORM\Column(length: 180)]
    private ?string $lastname = null;

    #[Assert\Length(
        min: 9,
        max: 9,
        minMessage: 'Numer telefonu musi skaładać się z{{ limit }} znaków',
        maxMessage: 'Numer telefonu musi skaładać się z{{ limit }} znaków',
    )]
    #[Assert\Regex(
        pattern: "/^\d+$/",
        message: "Numer telefonu musi składać się tylko z cyfr"
    )]
    #[ORM\Column(unique: true)]
    private ?string $phone = null;

    #[ORM\Column]
    private ?DateTime $creationdate = null;


    #[ORM\OneToMany(mappedBy: 'owner', targetEntity: Car::class, orphanRemoval: true)]
    private Collection $cars;

    #[ORM\OneToOne(mappedBy: 'owner', cascade: ['persist', 'remove'])]
    private ?Photo $photo = null;

    #[ORM\OneToMany(mappedBy: 'user', targetEntity: Transaction::class)]
    private Collection $transactions;

    #[ORM\OneToMany(mappedBy: 'user', targetEntity: OpinionSeller::class, orphanRemoval: true)]
    private Collection $opinionSellers;


    public function __construct()
    {
        $this->cars = new ArrayCollection();
        $this->transactions = new ArrayCollection();
        $this->opinionSellers = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUsername(): ?string
    {
        return $this->username;
    }

    public function setUsername(string $username): static
    {
        $this->username = $username;

        return $this;
    }

    /**
     * A visual identifier that represents this user.
     *
     * @see UserInterface
     */
    public function getUserIdentifier(): string
    {
        return (string) $this->username;
    }

    /**
     * @see UserInterface
     */
    public function getRoles(): array
    {
        $roles = $this->roles;
        // guarantee every user at least has ROLE_USER
        $roles[] = 'ROLE_USER';

        return array_unique($roles);
    }

    public function setRoles(array $roles): static
    {
        $this->roles = $roles;

        return $this;
    }

    /**
     * @see PasswordAuthenticatedUserInterface
     */
    public function getPassword(): string
    {
        return $this->password;
    }

    public function setPassword(string $password): static
    {
        $this->password = $password;

        return $this;
    }

    /**
     * @see UserInterface
     */
    public function eraseCredentials(): void
    {
        // If you store any temporary, sensitive data on the user, clear it here
        // $this->plainPassword = null;
    }

    /**
     * @return Collection<int, Car>
     */
    public function getCars(): Collection
    {
        return $this->cars;
    }

    public function addCar(Car $car): static
    {
        if (!$this->cars->contains($car)) {
            $this->cars->add($car);
            $car->setOwner($this);
        }

        return $this;
    }

    public function removeCar(Car $car): static
    {
        if ($this->cars->removeElement($car)) {
            // set the owning side to null (unless already changed)
            if ($car->getOwner() === $this) {
                $car->setOwner(null);
            }
        }

        return $this;
    }

    public function getEmail(): ?string
    {
        return $this->email;
    }

    public function setEmail(?string $email): self
    {
        $this->email = $email;
        return $this;
    }

    /**
     * @return string|null
     */
    public function getName(): ?string
    {
        return $this->name;
    }

    /**
     * @param string|null $name
     */
    public function setName(?string $name): void
    {
        $this->name = $name;
    }

    /**
     * @return string|null
     */
    public function getLastname(): ?string
    {
        return $this->lastname;
    }

    /**
     * @param string|null $lastname
     */
    public function setLastname(?string $lastname): void
    {
        $this->lastname = $lastname;
    }

    /**
     * @return string|null
     */
    public function getPhone(): ?string
    {
        return $this->phone;
    }

    /**
     * @param string|null $phone
     */
    public function setPhone(?string $phone): void
    {
        $this->phone = $phone;
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

    public function getPhoto(): ?Photo
    {
        return $this->photo;
    }

    public function setPhoto(?Photo $photo): static
    {
        // unset the owning side of the relation if necessary
        if ($photo === null && $this->photo !== null) {
            $this->photo->setOwner(null);
        }

        // set the owning side of the relation if necessary
        if ($photo !== null && $photo->getOwner() !== $this) {
            $photo->setOwner($this);
        }

        $this->photo = $photo;

        return $this;
    }

    /**
     * @return Collection<int, Transaction>
     */
    public function getTransactions(): Collection
    {
        return $this->transactions;
    }

    public function addTransaction(Transaction $transaction): static
    {
        if (!$this->transactions->contains($transaction)) {
            $this->transactions->add($transaction);
            $transaction->setUser($this);
        }

        return $this;
    }

    public function removeTransaction(Transaction $transaction): static
    {
        if ($this->transactions->removeElement($transaction)) {
            // set the owning side to null (unless already changed)
            if ($transaction->getUser() === $this) {
                $transaction->setUser(null);
            }
        }

        return $this;
    }

    /**
     * @return Collection<int, OpinionSeller>
     */
    public function getOpinionSellers(): Collection
    {
        return $this->opinionSellers;
    }

    public function addOpinionSeller(OpinionSeller $opinionSeller): static
    {
        if (!$this->opinionSellers->contains($opinionSeller)) {
            $this->opinionSellers->add($opinionSeller);
            $opinionSeller->setUser($this);
        }

        return $this;
    }

    public function removeOpinionSeller(OpinionSeller $opinionSeller): static
    {
        if ($this->opinionSellers->removeElement($opinionSeller)) {
            // set the owning side to null (unless already changed)
            if ($opinionSeller->getUser() === $this) {
                $opinionSeller->setUser(null);
            }
        }

        return $this;
    }
}
