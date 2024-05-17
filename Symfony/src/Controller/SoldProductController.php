<?php

namespace App\Controller;

use App\Entity\Transaction;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class SoldProductController extends AbstractController
{
    #[Route('/sold/product', name: 'app_sold_product')]
    public function index(Request $request, EntityManagerInterface $entityManager): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $seller = $entityManager->getRepository(Transaction::class)->findOneBy(['seller_id' => $user]);
        $transactions = $entityManager->getRepository(Transaction::class)->findBy(['seller_id'=>$user->getId()]);
        $groupedTransactions = [];

        foreach ($transactions as $transaction)
        {
            $dateKey = $transaction->getCreationDate()->format('d-m-Y H:i:s');
            $groupedTransactions[$dateKey][] = $transaction;
        }

        krsort($groupedTransactions);
        $renderData = [];

        foreach ($groupedTransactions as $date => $transactionsInDate)
        {
            $totalValue = 0;
            $transactionsData = [];
            foreach ($transactionsInDate as $transaction)
            {
                $transactionData = [
                    'id' => $transaction->getId(),
                    'product' => $transaction->getProduct(),
                    'quantity' => $transaction->getQuantity(),
                    'price' => $transaction->getPrice(),
                    'imageURL' => $transaction->getPhotoPath(),
                    'user' => $transaction->getUserlogin(),
                ];
                $transactionsData[] = $transactionData;
                $totalValue +=  $transaction->getQuantity() * $transaction->getPrice();
            }
            $renderData[] = [
                'date' => $date,
                'transactions' => $transactionsData,
                'totalValue'=>$totalValue,
            ];
        }

        return $this->render('sold_product/index.html.twig', [
            'soldProduct' => $renderData,
        ]);
    }
}
