<?php

namespace App\Controller;

use App\Form\UserEditTwoType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

class EditDataTwoController extends AbstractController
{
    #[Route('/edit/data/person', name: 'app_edit_data_person')]
    public function edit(Request $request, EntityManagerInterface $entityManager, UserPasswordHasherInterface $userPasswordHasher, ValidatorInterface $validator): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $form = $this->createForm(UserEditTwoType::class, $user);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid())
        {
            $plainPassword = $form->get('password')->getData();

            if (!$userPasswordHasher->isPasswordValid($user, $plainPassword))
            {
                $this->addFlash('error', 'Nieprawidłowe hasło.');
            }
            else
            {
                $entityManager->flush();
                $this->addFlash('success', 'Dane zostały zaktualizowane.');
            }
        }

        return $this->render('edit_data_2/index.html.twig', [
            'editDataTwo' => $form->createView(),
        ]);
    }
}

