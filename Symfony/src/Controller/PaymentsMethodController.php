<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

class PaymentsMethodController extends AbstractController
{
    #[Route('/payments/method', name: 'app_payments_method')]
    public function index(Request $request, SessionInterface $session): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);

        if (empty($cart))
        {
            $this->addFlash('error', 'Koszyk jest pusty.');
            return new RedirectResponse($this->generateUrl('app_cart_show'));
        }

        $session = $request->getSession();
        $totalValue = $session->get('totalValue');
        
        return $this->render('payments_method/index.html.twig', [
            'totalValue'=>$totalValue,
        ]);
    }
}
