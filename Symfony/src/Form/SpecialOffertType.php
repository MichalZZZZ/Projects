<?php

namespace App\Form;

use App\Entity\SpecialOffert;
use Doctrine\DBAL\Types\TextType;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;


class SpecialOffertType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('code', \Symfony\Component\Form\Extension\Core\Type\TextType::class, [
                'label'=> 'KOD: '
            ])
//            ->add('value', NumberType::class, [
//                'mapped'=>false,
//                'required'=>false
//            ])
        ;
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => SpecialOffert::class,
        ]);
    }
}
