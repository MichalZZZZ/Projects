<?php

namespace App\Repository;

use App\Entity\SpecialOffert;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<SpecialOffert>
 *
 * @method SpecialOffert|null find($id, $lockMode = null, $lockVersion = null)
 * @method SpecialOffert|null findOneBy(array $criteria, array $orderBy = null)
 * @method SpecialOffert[]    findAll()
 * @method SpecialOffert[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class SpecialOffertRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, SpecialOffert::class);
    }

    public function save(SpecialOffert $entity, bool $flush = false): void
    {
        $this->getEntityManager()->persist($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }

    public function remove(SpecialOffert $entity, bool $flush = false): void
    {
        $this->getEntityManager()->remove($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }

//    /**
//     * @return SpecialOffert[] Returns an array of SpecialOffert objects
//     */
//    public function findByExampleField($value): array
//    {
//        return $this->createQueryBuilder('s')
//            ->andWhere('s.exampleField = :val')
//            ->setParameter('val', $value)
//            ->orderBy('s.id', 'ASC')
//            ->setMaxResults(10)
//            ->getQuery()
//            ->getResult()
//        ;
//    }

//    public function findOneBySomeField($value): ?SpecialOffert
//    {
//        return $this->createQueryBuilder('s')
//            ->andWhere('s.exampleField = :val')
//            ->setParameter('val', $value)
//            ->getQuery()
//            ->getOneOrNullResult()
//        ;
//    }
}
