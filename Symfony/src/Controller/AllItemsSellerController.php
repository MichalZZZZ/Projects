<?php

namespace App\Controller;

use App\Entity\Car;
use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class AllItemsSellerController extends AbstractController
{
    #[Route('/all/items/seller/{id}', name: 'app_all_items_seller')]
    public function index(EntityManagerInterface $entityManager, $id): Response
    {
        $allItems = $entityManager->getRepository(Car::class)->findBy(['owner' => $id]);
        $seller = $entityManager->getRepository(User::class)->find($id);
        $ListItems = [];
        if (!$seller)
        {
            $this->addFlash('error', 'Sprzedający o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }
        else if (count($allItems) == 0)
        {
            $this->addFlash('error', 'Sprzedający nie posiada żadnych przedmiotów na sprzedaż');
        }
        else
        {
            foreach ($allItems as $item)
            {
                $ListItems[] = [
                    'item'=>$item,
                    'imageURL'=>$item->getPhotoPath(),
                ];
            }
        }

        return $this->render('all_items_seller/index.html.twig', [
            'listItems'=>$ListItems,
            'seller'=>$seller->getUsername(),
        ]);
    }
}
