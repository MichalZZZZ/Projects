<?php

namespace App\Controller;

use App\Form\PasswordUpdateForm;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

class UpdatePasswordController extends AbstractController
{
    #[Route('/update/password', name: 'app_update_password')]
    public function updatePassword(Request $request, EntityManagerInterface $entityManager, UserPasswordHasherInterface $userPasswordHasher): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $form = $this->createForm(PasswordUpdateForm::class);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $plainPassword = $form->get('oldPassword')->getData();
            $newPassword = $form->get('password')->getData();
            $confirmPassword = $form->get('confirmPassword')->getData();

            if (!$userPasswordHasher->isPasswordValid($user, $plainPassword))
            {
                $this->addFlash('error', 'Nieprawidlowe haslo');
            }
            else if ($newPassword != $confirmPassword)
            {
                $this->addFlash('error', 'Hasla sa niezgodne');
            }
            else
            {
                $hashedPassword = $userPasswordHasher->hashPassword($user, $newPassword);
                $user->setPassword($hashedPassword);

                $entityManager->persist($user);
                $entityManager->flush();
                $this->addFlash('success', 'Haslo zostalo zmienione');
            }
        }

        return $this->render('update_password/index.html.twig', [
            'updatePassword' => $form->createView(),
        ]);
    }
}