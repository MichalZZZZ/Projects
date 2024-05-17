<?php

namespace App\Form;

use App\Entity\Car;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class EditCarForm extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
//        $car = $options['car'];
        $builder
            ->add('photopath', TextType::class, [
                'label' => 'Photo Path',
//                'data' => $car->getPhotopath()
            ])
            ->add('price', TextType::class, [
                'label' => 'Price',
            ])
            ->add('description', TextareaType::class, [
                'label' => 'Description',
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'data_class' => Car::class,
        ]);
    }
}


