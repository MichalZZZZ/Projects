<?php

namespace App\Controller;

use App\Entity\User;
use App\Entity\OpinionSeller;
use App\Form\OpinionFormType;
use App\Repository\OpinionSellerRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

class ShowSellerController extends AbstractController
{
    #[Route('/show/seller/{id}/comments/{page}', name: 'app_show_seller')]
    public function index(Request $request, EntityManagerInterface $entityManager, $page, OpinionSellerRepository $opinionSellerRepository, $id): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $entityManager->getRepository(User::class)->find($id);

        if (!$user)
        {
            $this->addFlash('error', 'Sprzedający o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }


        $paginatorPerPage = OpinionSellerRepository::PAGINATOR_PER_PAGE;
        $offset = ($page - 1) * $paginatorPerPage;
        $commentPaginator = $opinionSellerRepository->getCommentPaginator($user, $offset);
        $totalItems = count($commentPaginator);
        $totalPages = ceil($totalItems / $paginatorPerPage);

        if ($page > $totalPages and $totalPages >= 1)
        {
            $this->addFlash('error', 'Taka strona nie istnieje.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        $opinionUser = $entityManager->getRepository(OpinionSeller::class)->findBy(['user'=>$user->getId()], ['id'=> 'DESC']);
        $mean = 0;
        $percent = 0;
        $value = 0;

        foreach ($opinionUser as $opinion)
        {
            $value += $opinion->getScale();
        }

        if ($opinionUser)
        {
            $count = count($opinionUser);
            $mean = round(($value / $count), 2);
            $percent = round(($mean / 5) * 100, 2);
        }

        $opinion = new OpinionSeller();
        $form = $this->createForm(OpinionFormType::class, $opinion);
        $form->handleRequest($request);
        $flag = true;

        if($user->getId() == $this->getUser()->getId())
        {
            $flag = false;
        }
        else
        {
            if ($form->isSubmitted() && $form->isValid())
            {
                $opinion->setUser($user);
                $opinion->setLoginadduser($this->getUser()->getUsername());
                $opinion->setLoginuser($user->getUsername());
                $opinion->setCreationdate(new \DateTime());
                $entityManager->persist($opinion);
                $entityManager->flush();
                $this->addFlash('success', 'Dziękujemy za dodanie opini.');
            }
        }

        return $this->render('show_seller/index.html.twig', [
            'user'=>$user,
            'form' => $form->createView(),
            'flag'=>$flag,
            'opinion'=>$opinionUser,
            'mean'=> $mean,
            'percent'=> $percent,
            'comments' => $commentPaginator,
            'page' => $page,
            'totalPages' => $totalPages,
        ]);
    }
}
