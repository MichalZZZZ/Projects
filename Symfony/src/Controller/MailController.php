<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Mailer\Transport;
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mime\Email;

class MailController extends AbstractController
{
    #[Route('/mail', name: 'app_mail')]
    public function index(Request $request): Response
    {
        $transport = Transport::fromDSN('smtp://michal.jakis123.123@gmail.com:qoqlmgcanjlsgpro@smtp.gmail.com:587');
        $mailer = new Mailer($transport);
        $email = (new Email());

        if ($request->isMethod('POST'))
        {
            $userName = $this->getUser()->getUsername();
            $emailUser = $this->getUser()->getEmail();
            $email->from($emailUser);
            $email->to('michal.jakis123.123@gmail.com');
            $email->subject('Wiadomość od użytkownika: '. $userName.', '.$emailUser.': '. $request->get('theme'));
            $email->text($request->get('contents'));
//            $mailer->send($email);
            
//            if($mailer)
//            {
//                $this->addFlash('success', 'Dziękujemy za kontakt.');
//            }
//            else
//            {
//                $this->addFlash('error', 'Wystąpił błąd.');
//            }
        }

        return $this->render('mail/index.html.twig', [
        ]);
    }
    
}
