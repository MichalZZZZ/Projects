<?php

namespace App\Controller;

use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;


class IndexController extends AbstractController
{
    #[Route('/', name: 'index')]
    public function index(EntityManagerInterface $entityManager, Request $request): Response
    {
        $allUser = $entityManager->getRepository(User::class)->findBy([], ['creationdate' => 'DESC'], 7);

        return $this->render('index/index.html.twig', [
            'allUser'=>$allUser,
        ]);
    }
}
