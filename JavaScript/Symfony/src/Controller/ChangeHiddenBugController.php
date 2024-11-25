<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Bugs;

class ChangeHiddenBugController extends AbstractController
{
    #[Route('/change/status/bug/{id}', name: 'app_change_status_bug')]
    public function changeHidden(int $id, EntityManagerInterface $entityManager): Response
    {
        $repository = $entityManager->getRepository(Bugs::class);
        $changeBug = $repository->findOneBy(['hidden' => 0, 'id' => $id]);
        $changeBug->setHidden(1);
        $entityManager->persist($changeBug);
        $entityManager->flush();

        return $this->redirectToRoute('app_show_bugs');
    }
}
