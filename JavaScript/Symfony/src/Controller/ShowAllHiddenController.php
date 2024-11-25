<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\HttpFoundation\JsonResponse;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Bugs;

class ShowAllHiddenController extends AbstractController
{
    #[Route('/show/all/hidden', name: 'app_show_all_hidden')]
    public function index(EntityManagerInterface $entityManager): Response
    {
        $repository = $entityManager->getRepository(Bugs::class);
        $bugsHidden = $repository->findBy(['hidden' => 1]);

        if (!$bugsHidden) {
            return new JsonResponse(['status' => 'error', 'message' => 'No hidden bugs found'], JsonResponse::HTTP_NOT_FOUND);
        }

        return $this->render('show_all_hidden/index.html.twig', [
            'bugsHidden' => $bugsHidden,
        ]);
    }
}
