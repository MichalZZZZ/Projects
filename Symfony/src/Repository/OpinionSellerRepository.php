<?php

namespace App\Repository;

use App\Entity\OpinionSeller;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;
use App\Entity\User;
use Doctrine\ORM\Tools\Pagination\Paginator;

/**
 * @extends ServiceEntityRepository<OpinionSeller>
 *
 * @method OpinionSeller|null find($id, $lockMode = null, $lockVersion = null)
 * @method OpinionSeller|null findOneBy(array $criteria, array $orderBy = null)
 * @method OpinionSeller[]    findAll()
 * @method OpinionSeller[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class OpinionSellerRepository extends ServiceEntityRepository
{
    public const PAGINATOR_PER_PAGE = 3;

    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, OpinionSeller::class);
    }

    public function getCommentPaginator(User $user, int $offset): Paginator
    {
        $query = $this->createQueryBuilder('c')
            ->andWhere('c.user = :user')
            ->setParameter('user', $user)
            ->orderBy('c.creationdate', 'DESC')
           ->setMaxResults(self::PAGINATOR_PER_PAGE)
           ->setFirstResult($offset)
            ->getQuery()
        ;
        return new Paginator($query);
    }

    public function save(OpinionSeller $entity, bool $flush = false): void
    {
        $this->getEntityManager()->persist($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }

    public function remove(OpinionSeller $entity, bool $flush = false): void
    {
        $this->getEntityManager()->remove($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }

//    /**
//     * @return OpinionSeller[] Returns an array of OpinionSeller objects
//     */
//    public function findByExampleField($value): array
//    {
//        return $this->createQueryBuilder('o')
//            ->andWhere('o.exampleField = :val')
//            ->setParameter('val', $value)
//            ->orderBy('o.id', 'ASC')
//            ->setMaxResults(10)
//            ->getQuery()
//            ->getResult()
//        ;
//    }

//    public function findOneBySomeField($value): ?OpinionSeller
//    {
//        return $this->createQueryBuilder('o')
//            ->andWhere('o.exampleField = :val')
//            ->setParameter('val', $value)
//            ->getQuery()
//            ->getOneOrNullResult()
//        ;
//    }
}
