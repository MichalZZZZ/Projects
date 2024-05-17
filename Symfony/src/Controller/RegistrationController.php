<?php

namespace App\Controller;

use App\Entity\User;
use App\Form\RegistrationFormType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mailer\Transport;
use Symfony\Component\Mime\Email;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Contracts\Translation\TranslatorInterface;

class RegistrationController extends AbstractController
{
    #[Route('/register', name: 'app_register')]
    public function register(Request $request, UserPasswordHasherInterface $userPasswordHasher, EntityManagerInterface $entityManager, ValidatorInterface $validator): Response
    {
        $user = new User();
        $form = $this->createForm(RegistrationFormType::class, $user);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid())
        {
            $user->setPassword($userPasswordHasher->hashPassword($user, $form->get('plainPassword')->getData()));
            $user->setRoles(['ROLE_USER']);
            $user->setCreationDate(new \DateTime());
            $entityManager->persist($user);
            $entityManager->flush();
            $this->addFlash('success', 'Dziękujemy za założenie konta.');
            $transport = Transport::fromDSN('smtp://michal.jakis123.123@gmail.com:qoqlmgcanjlsgpro@smtp.gmail.com:587');
            $mailer = new Mailer($transport);
            $email = (new Email());
            $email->from('michal.jakis123.123@gmail.com');
            $email->to($form->get('email')->getData());
            $email->subject('Witaj w Cars!');
            $email->text('Witamy cię '. $form->get('username')->getData() .'w naszym serwisie internetowym. Dziękujemy za założenie konta. Możesz się zalogować. Twoje dane logowania to: '.$form->get('username')->getData());
//            $mailer->send($email);
        }

        return $this->render('registration/register.html.twig', [
            'registrationForm' => $form->createView(),
        ]);
    }
}
