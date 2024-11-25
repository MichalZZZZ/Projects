<?php

namespace App\Controller;

use App\Entity\Bugs;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\JsonResponse;

class ShowBugsController extends AbstractController
{
    #[Route('/show/bugs', name: 'app_show_bugs')]
    public function index(EntityManagerInterface $entityManager): Response
    {
        $repository = $entityManager->getRepository(Bugs::class);
        $bugs = $repository->findBy(['hidden' => 0]);

        return $this->render('show_bugs/index.html.twig', [
            'bugs' => $bugs,
        ]);
    }
}