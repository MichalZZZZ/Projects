<?php

namespace App\Controller;

use App\Entity\Car;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class ShowCarController extends AbstractController
{
    #[Route('/show/car/{id}', name: 'app_show_car')]
    public function showCar(EntityManagerInterface $entityManager, $id): Response
    {
        $car = $entityManager->getRepository(Car::class)->find($id);

        if (!$car)
        {
            $this->addFlash('error', 'Produkt o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        $quantity = $car->getQuantity();
        $myCar = $car->getOwner();
        $flag = true;
        $user = $this->getUser();

        if ($user)
        {
            if($user == $myCar)
            {
                $flag = false;
            }
        }

        return $this->render('show_car/index.html.twig', [
            'ShowCars' => $car,
            'flaga'=>$flag,
            'quan'=>$quantity,
        ]);
    }
}
