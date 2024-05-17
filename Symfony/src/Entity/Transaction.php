<?php

namespace App\Entity;

use App\Repository\TransactionRepository;
use DateTime;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: TransactionRepository::class)]
class Transaction
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $product = null;

    #[ORM\Column]
    private ?int $quantity = null;

    #[ORM\Column]
    private ?float $price = null;

    #[ORM\Column(length: 255)]
    private ?string $photopath = null;

    #[ORM\Column]
    private ?DateTime $creationdate = null;

    #[ORM\Column]
    private ?string $userlogin = null;

    #[ORM\Column]
    private ?string $useremail = null;

    #[ORM\Column]
    private ?string $username = null;

    #[ORM\Column]
    private ?string $userlastname = null;

    #[ORM\Column]
    private ?int $userPhone = null;

    #[ORM\ManyToOne(inversedBy: 'transactions')]
    private ?User $user = null;





    #[ORM\Column]
    private ?string $sellerlogin = null;

    #[ORM\Column]
    private ?string $selleremail = null;

    #[ORM\Column]
    private ?string $sellername = null;

    #[ORM\Column]
    private ?string $sellerlastname = null;

    #[ORM\Column]
    private ?int $sellerPhone = null;

    #[ORM\Column]
    private ?int $seller_id = null;





    public function getId(): ?int
    {
        return $this->id;
    }

    public function getProduct(): ?string
    {
        return $this->product;
    }

    public function setProduct(string $product): static
    {
        $this->product = $product;

        return $this;
    }

    public function getQuantity(): ?int
    {
        return $this->quantity;
    }

    public function setQuantity(int $quantity): static
    {
        $this->quantity = $quantity;

        return $this;
    }

    public function getPrice(): ?float
    {
        return $this->price;
    }

    public function setPrice(float $price): static
    {
        $this->price = $price;

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
    public function getPhotopath(): ?string
    {
        return $this->photopath;
    }

    /**
     * @param string|null $photopath
     */
    public function setPhotopath(?string $photopath): void
    {
        $this->photopath = $photopath;
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

    /**
     * @return string|null
     */
    public function getUserlogin(): ?string
    {
        return $this->userlogin;
    }

    /**
     * @param string|null $userlogin
     */
    public function setUserlogin(?string $userlogin): void
    {
        $this->userlogin = $userlogin;
    }

    /**
     * @return string|null
     */
    public function getUseremail(): ?string
    {
        return $this->useremail;
    }

    /**
     * @param string|null $useremail
     */
    public function setUseremail(?string $useremail): void
    {
        $this->useremail = $useremail;
    }

    /**
     * @return string|null
     */
    public function getUsername(): ?string
    {
        return $this->username;
    }

    /**
     * @param string|null $username
     */
    public function setUsername(?string $username): void
    {
        $this->username = $username;
    }

    /**
     * @return string|null
     */
    public function getUserlastname(): ?string
    {
        return $this->userlastname;
    }

    /**
     * @param string|null $userlastname
     */
    public function setUserlastname(?string $userlastname): void
    {
        $this->userlastname = $userlastname;
    }

    /**
     * @return int|null
     */
    public function getUserPhone(): ?int
    {
        return $this->userPhone;
    }

    /**
     * @param int|null $userPhone
     */
    public function setUserPhone(?int $userPhone): void
    {
        $this->userPhone = $userPhone;
    }

    /**
     * @return string|null
     */
    public function getSelleremail(): ?string
    {
        return $this->selleremail;
    }

    /**
     * @param string|null $selleremail
     */
    public function setSelleremail(?string $selleremail): void
    {
        $this->selleremail = $selleremail;
    }

    /**
     * @return int|null
     */
    public function getSellerId(): ?int
    {
        return $this->seller_id;
    }

    /**
     * @param int|null $seller_id
     */
    public function setSellerId(?int $seller_id): void
    {
        $this->seller_id = $seller_id;
    }

    /**
     * @return string|null
     */
    public function getSellerlastname(): ?string
    {
        return $this->sellerlastname;
    }

    /**
     * @param string|null $sellerlastname
     */
    public function setSellerlastname(?string $sellerlastname): void
    {
        $this->sellerlastname = $sellerlastname;
    }

    /**
     * @return string|null
     */
    public function getSellerlogin(): ?string
    {
        return $this->sellerlogin;
    }

    /**
     * @param string|null $sellerlogin
     */
    public function setSellerlogin(?string $sellerlogin): void
    {
        $this->sellerlogin = $sellerlogin;
    }

    /**
     * @return string|null
     */
    public function getSellername(): ?string
    {
        return $this->sellername;
    }

    /**
     * @param string|null $sellername
     */
    public function setSellername(?string $sellername): void
    {
        $this->sellername = $sellername;
    }

    /**
     * @return int|null
     */
    public function getSellerPhone(): ?int
    {
        return $this->sellerPhone;
    }

    /**
     * @param int|null $sellerPhone
     */
    public function setSellerPhone(?int $sellerPhone): void
    {
        $this->sellerPhone = $sellerPhone;
    }
}
