<?php

namespace App\Controller;

use App\Entity\Car;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class MyCarsController extends AbstractController
{
    #[Route('/my/cars', name: 'app_my_cars')]
    public function index(EntityManagerInterface $entityManager): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $carData = [];
        $myCar = $entityManager->getRepository(Car::class)->findBy(['owner' => $this->getUser()]);

        if (count($myCar) == 0)
        {
            $this->addFlash('error', 'Nie masz żadnych samochodów');
        }
        else
        {
            foreach ($myCar as $car)
            {
                $quantity = $car->getQuantity();
                $carData[] = [
                    'car' => $car,
                    'imageUrl' => $car->getPhotopath(),
                    'quan'=>$quantity,
                ];
            }
        }

        return $this->render('my_cars/index.html.twig', [
            'MyCars' => $carData,
        ]);
    }

    #[Route('/my/cars/delete/{id}', name: 'app_my_cars_delete')]
    public function deleteCar(EntityManagerInterface $entityManager, $id): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $car = $entityManager->getRepository(Car::class)->find($id);

        if (!$car) {
            $this->addFlash('error', 'Samochód o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }
        else
        {
            $entityManager->remove($car);
            $entityManager->flush();
            $this->addFlash('error', 'Samochód został usunięty.');
        }
        return $this->redirectToRoute('app_my_cars');
    }
}
