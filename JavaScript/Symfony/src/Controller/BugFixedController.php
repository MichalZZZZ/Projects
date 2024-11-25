<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Bugs;

class BugFixedController extends AbstractController
{
    #[Route('/bug/fixed/{id}', name: 'app_bug_fixed')]
    public function index(int $id, EntityManagerInterface $entityManager): Response
    {
        $repository = $entityManager->getRepository(Bugs::class);
        $bugs = $repository->findOneBy(['hidden' => 0, 'id' => $id]);

        if (!$bugs) {
            return new JsonResponse(['status' => 'error', 'message' => 'No bugs found'], JsonResponse::HTTP_NOT_FOUND);
        }
        else{
            $bugs->setStatus('Done');
            $entityManager->persist($bugs);
            $entityManager->flush();
            $this->addFlash('success', 'Bug fixed successfully');
        }

        return $this->render('show_one_bug/index.html.twig', [
            'bug' => $bugs,
        ]);
    }
}
