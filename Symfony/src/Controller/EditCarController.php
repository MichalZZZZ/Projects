<?php

namespace App\Controller;

use App\Entity\Car;
use App\Form\EditCarForm;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class EditCarController extends AbstractController
{
    #[Route('/edit/car/{id}', name: 'app_edit_car')]
    public function index(Request $request, EntityManagerInterface $entityManager, $id): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $car = $entityManager->getRepository(Car::class)->find($id);

        if (!$car)
        {
            $this->addFlash('error', 'Samochód o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        $photo = $car->getPhotoPath();
        $form = $this->createForm(EditCarForm::class, $car);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid())
        {
            $newPhoto = $form->get('photopath')->getData();
            $newDescription = $form->get('description')->getData();
            $car->setPhotoPath($newPhoto);
            $car->setDescription($newDescription);
            $entityManager->flush();
            $this->addFlash('success', 'Dane zostaly zaktualizowane.');
        }

        return $this->render('edit_car/index.html.twig', [
            'editCars' => $form->createView(),
            'photo' => $photo
        ]);
    }
}
