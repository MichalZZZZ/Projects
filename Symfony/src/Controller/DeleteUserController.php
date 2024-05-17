<?php

namespace App\Controller;

use App\Entity\Transaction;
use App\Form\UserDelete;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;
use Symfony\Component\HttpFoundation\Session\SessionInterface;

class DeleteUserController extends AbstractController
{
    #[Route('/delete/user', name: 'app_delete_user')]
    public function delete(Request $request, EntityManagerInterface $entityManager, UserPasswordHasherInterface $userPasswordHasher, TokenStorageInterface $tokenStorage, SessionInterface $session): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $form = $this->createForm(UserDelete::class);
        $form->handleRequest($request);
        $transactions = $entityManager->getRepository(Transaction::class)->findBy(['user'=>$this->getUser()]);

        if ($form->isSubmitted() && $form->isValid())
        {
            $user = $this->getUser();
            $plainPassword = $form->get('password')->getData();
            $confirmPassword = $form->get('passwordConfirm')->getData();

            if (!$userPasswordHasher->isPasswordValid($user, $plainPassword))
            {
                $this->addFlash('error', 'Nieprawidłowe hasło.');
            }
            if ($plainPassword != $confirmPassword)
            {
                $this->addFlash('error', 'Hasła są niezgodne');
            }
            else
            {
                $confirm = $request->request->get('confirm');

                if ($confirm === 'true')
                {
                    foreach ($transactions as $item)
                    {
                        $item->setUser(null);
                    }
                    $entityManager->remove($user);
                    $entityManager->flush();

                    $tokenStorage->setToken(null);
                    $session->invalidate();

                    return $this->redirectToRoute('index');
                }
                elseif ($confirm === 'false')
                {
                    return $this->redirectToRoute('app_my_profile');
                }
            }
        }

        return $this->render('delete_user/confirm_delete.html.twig', [
            'deleteData' => $form->createView(),
        ]);
    }
}


