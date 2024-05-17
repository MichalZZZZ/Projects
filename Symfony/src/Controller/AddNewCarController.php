<?php

namespace App\Controller;

use App\Entity\Car;
use App\Form\AddCarForm;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

class AddNewCarController extends AbstractController
{
    #[Route('/add/new/car', name: 'app_add_new_car')]
    public function index(Request $request, EntityManagerInterface $entityManager)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $car = new Car();
        $form = $this->createForm(AddCarForm::class, $car);
        $form->handleRequest($request);
        $carCount = $entityManager->getRepository(Car::class)->count(['owner' => $this->getUser()]);

        if ($form->isSubmitted() && $form->isValid())
        {
            if ($carCount >= 10)
            {
                $response = ['error' => true, 'message' => 'Możesz dodać maksymalnie 10 aut.'];
                return new JsonResponse($response);
            }
            else
            {
                if ($this->getUser())
                {
                    $car->setOwner($this->getUser());
                    $car->setCreationDate(new \DateTime());
                    $car->setStatus('dostepny');
                    $entityManager->persist($car);
                    $entityManager->flush();
                    $response = ['success' => true, 'message' => 'Samochód został dodany!'];
                    return new JsonResponse($response);
                }
                else
                {
                    $response = ['error' => true, 'message' => 'Wystąpił błąd!'];
                    return new JsonResponse($response);
                }
            }
        }

        return $this->render('add_new_car/index.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
