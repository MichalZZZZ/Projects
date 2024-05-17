<?php
//
//namespace App\Controller;
//
//use App\Entity\User;
//use App\Form\UserEditType;
//use Doctrine\ORM\EntityManagerInterface;
//use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
//use Symfony\Component\HttpFoundation\Request;
//use Symfony\Component\HttpFoundation\Response;
//use Symfony\Component\Routing\Annotation\Route;
//use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
//
//
//class EditDataController extends AbstractController
//{
//    #[Route('/edit/data', name: 'app_edit_data')]
//    public function edit(Request $request, EntityManagerInterface $entityManager,  UserPasswordHasherInterface $userPasswordHasher): Response
//    {
//        $user = $this->getUser();
//        $form = $this->createForm(UserEditType::class, $user);
//        $form->handleRequest($request);
//
//        $this->denyAccessUnlessGranted('ROLE_USER');
//
//            if ($form->isSubmitted() && $form->isValid())
//            {
//                $plainPassword = $form->get('password')->getData(); // Wprowadzone hasło z formularza
//                if (!$userPasswordHasher->isPasswordValid($user, $plainPassword)) {
//                    $this->addFlash('error', 'Nieprawidłowe hasło.');
//                }
//                else
//                {
//                    $entityManager->flush();
//                    $this->addFlash('success', 'Dane zostały zaktualizowane.');
//                    return $this->redirectToRoute('app_edit_data');
//                }
//            }
////            else{$this->addFlash('error', 'Błąd.');}
//
//        return $this->render('edit_data/index.html.twig', [
//            'editData' => $form->createView(),
//        ]);
//    }
//}
//


namespace App\Controller;

use App\Entity\User;
use App\Form\UserEditType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

class EditDataController extends AbstractController
{
    #[Route('/edit/data', name: 'app_edit_data')]
    public function edit(Request $request, EntityManagerInterface $entityManager, UserPasswordHasherInterface $userPasswordHasher, ValidatorInterface $validator): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $form = $this->createForm(UserEditType::class, $user);
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

        return $this->render('edit_data/index.html.twig', [
            'editData' => $form->createView(),
        ]);
    }
}

