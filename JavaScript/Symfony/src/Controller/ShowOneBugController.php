<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Bugs;

class ShowOneBugController extends AbstractController
{
    #[Route('/show/one/{id}', name: 'app_show_one_bug')]
    public function index(int $id, EntityManagerInterface $entityManager): Response
    {
        $repository = $entityManager->getRepository(Bugs::class);
        $bug = $repository->find($id);
        
        if (!$bug) {
            throw $this->createNotFoundException('Bug not found');
        }
    
        return $this->render('show_one_bug/index.html.twig', [
            'bug' => $bug,
        ]);
    }
}
