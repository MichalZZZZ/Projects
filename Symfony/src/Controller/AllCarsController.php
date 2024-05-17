<?php

namespace App\Controller;

use App\Entity\Car;
use App\Form\SearchTypeForm;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;


class AllCarsController extends AbstractController
{
    #[Route('/all/cars', name: 'app_all_cars')]
    public function index(Request $request, EntityManagerInterface $entityManager): Response
    {
        $form = $this->createForm(SearchTypeForm::class);
        $form->handleRequest($request);
        $allCar = [];
        $repository = $entityManager->getRepository(Car::class);
        $latestCars = $repository->findBy([], ['creationdate' => 'DESC'], 5);
        
        if ($form->isSubmitted() && $form->isValid())
        {
            $data = $form->getData();
            $brand = $data['query'];
            $searchQuery = $brand;
            $allCar3 = $entityManager->getRepository(Car::class)->createQueryBuilder('c')
                ->where('c.name LIKE :searchQuery OR c.model LIKE :searchQuery')
                ->setParameter('searchQuery', '%' . $searchQuery . '%')
                ->getQuery()
                ->getResult();

            foreach ($allCar3 as $car)
            {
                $quantity = $car->getQuantity();
                $allCar[] = [
                    'car' => $car,
                    'imageUrl' => $car->getPhotopath(),
                    'quan'=>$quantity,
                ];
            }

            if (!$allCar)
            {
                $this->addFlash('error','Nie znaleziono żadnych pasującyh wyników');
            }
        }
        else if ($request->isMethod('POST'))
        {
            $name = $request->get('name');
            $model = $request->get('model');
            $priceMin = $request->get('price-min');
            $priceMax = $request->get('price-max');
            $queryBuilder = $entityManager->getRepository(Car::class)->createQueryBuilder('c');

            if ($name) {
                $queryBuilder->andWhere('c.name LIKE :name');
                $queryBuilder->setParameter('name', '%' . $name . '%');
            }

            if ($model) {
                $queryBuilder->andWhere('c.model = :model');
                $queryBuilder->setParameter('model', $model);
            }

            if ($priceMin !== null) {
                $queryBuilder->andWhere('c.price >= :priceMin');
                $queryBuilder->setParameter('priceMin', $priceMin);
            }

            if ($priceMax !== null) {
                $queryBuilder->andWhere('c.price <= :priceMax');
                $queryBuilder->setParameter('priceMax', $priceMax);
            }

            $allCar2 = $queryBuilder->getQuery()->getResult();

            foreach ($allCar2 as $car)
            {
                $quantity = $car->getQuantity();
                $allCar[] = [
                    'car' => $car,
                    'imageUrl' => $car->getPhotopath(),
                    'quan'=>$quantity,
                ];
            }

            if (!$allCar)
            {
                $this->addFlash('error','Nie znaleziono żadnych pasującyh wyników');
            }
        }
        else
        {
            $allCars = $entityManager->getRepository(Car::class)->findAll();
            foreach ($allCars as $car)
            {
                $quantity = $car->getQuantity();
                $allCar[] = [
                    'car' => $car,
                    'imageUrl' => $car->getPhotopath(),
                    'quan'=>$quantity,
                ];
            }
        }

        return $this->render('all_cars/index.html.twig', [
            'AllCars' => $allCar,
            'latestCars'=>$latestCars,
            'form' => $form->createView(),
        ]);
    }


    #[Route('/all/filter/view', name: 'app_filter_view')]
    public function viewCars(Request $request, EntityManagerInterface $entityManager): Response
    {
        return $this->render('filter_cars/index.html.twig', [
        ]);
    }
}
