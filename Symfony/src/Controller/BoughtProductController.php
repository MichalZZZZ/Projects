<?php

namespace App\Controller;

use App\Entity\Transaction;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class BoughtProductController extends AbstractController
{
    #[Route('/bought/product', name: 'app_bought_product')]
    public function index(Request $request, EntityManagerInterface $entityManager): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $transactions = $entityManager->getRepository(Transaction::class)
            ->createQueryBuilder('t')
            ->where('t.user = :user')
            ->setParameter('user', $user)
            ->orderBy('t.creationdate', 'ASC')
            ->getQuery()
            ->getResult();

        $groupedTransactions = [];

        foreach ($transactions as $transaction) {
            $dateKey = $transaction->getCreationDate()->format('d-m-Y H:i:s');
            $groupedTransactions[$dateKey][] = $transaction;
        }

        krsort($groupedTransactions);
        $renderData = [];

        foreach ($groupedTransactions as $date => $transactionsInDate) {
            $totalValue = 0;
            $transactionsData = [];

            foreach ($transactionsInDate as $transaction) {
                $transactionData = [
                    'id' => $transaction->getId(),
                    'product' => $transaction->getProduct(),
                    'quantity' => $transaction->getQuantity(),
                    'price' => $transaction->getPrice(),
                    'imageURL' => $transaction->getPhotoPath(),
                    'seller' => $transaction->getSellerlogin(),
                ];
                $transactionsData[] = $transactionData;
                $totalValue += $transaction->getQuantity() * $transaction->getPrice();
            }
            $renderData[] = [
                'date' => $date,
                'transactions' => $transactionsData,
                'totalValue' => $totalValue,
            ];
        }

        return $this->render('bought_product/index.html.twig', [
            'boughtProduct' => $renderData,
        ]);
    }
}
