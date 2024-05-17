<?php

namespace App\Controller;

use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Mailer\Exception\TransportExceptionInterface;
use Symfony\Component\Mailer\Transport;
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mime\Email;


class RemindPasswordController extends AbstractController
{
    #[Route('/remind/password', name: 'app_remind_password')]
    public function index(Request $request, EntityManagerInterface $entityManager, UserPasswordHasherInterface $userPasswordHasher): Response
    {
        if ($request->isMethod('POST'))
        {
            $userName = $request->get('login');
            $emailSend = $request->get('email');
            $checkUser = $entityManager->getRepository(User::class)->findOneBy(['username' => $userName, 'email' => $emailSend]);

            if($checkUser)
            {
                $resetPassword = ('cY$l#9');
                $checkUser->setPassword($userPasswordHasher->hashPassword($checkUser, $resetPassword));
                $entityManager->flush();
                $transport = Transport::fromDSN('smtp://michal.jakis123.123@gmail.com:qoqlmgcanjlsgpro@smtp.gmail.com:587');
                $mailer = new Mailer($transport);
                $email = (new Email());
                $email->from('michal.jakis123.123@gmail.com');
                $email->to($emailSend);
                $email->subject('Nowe hasło');
                $email->text('Twoje nowe hasło to: '.$resetPassword);
//                $mailer->send($email);
//
//                if($mailer)
//                {
//                    $this->addFlash('success', 'Wysłaliśmy wiadomość na twój adres e-mail.');
//                }
//                else
//                {
//                    $this->addFlash('error', 'Wystąpił błąd.');
//                }
            }
            else
            {
                $this->addFlash('error', 'Nie znaleźliśmy takiego konta');
            }
        }

        return $this->render('remind_password/index.html.twig', [
        ]);
    }
}
